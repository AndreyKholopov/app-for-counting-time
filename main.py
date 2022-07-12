from kivymd.app import MDApp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem

from database import Database

db = Database()

class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def show_change_task_dialog(self, the_list_item):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Change Task",
                type="custom",
                content_cls=DialogChangeContent(the_list_item),
            )

        self.task_list_dialog.open()

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
        
    def on_start(self):
        try:
            tasks = db.get_tasks()

            if tasks != []:
                for task in tasks:
                    add_task = ListItem(pk=task[0], text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

        except Exception as e:
            print(e)
            pass

    def add_task(self, task):
        created_task = db.create_task(task.text, 0)

        self.root.ids['container'].add_widget(ListItem(pk=created_task[0], text=created_task[1], secondary_text=created_task[2]))
        task.text = ''


class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DialogChangeContent(MDBoxLayout):
    def __init__(self, the_list_item, **kwargs):
        super().__init__(**kwargs)
        print(self)
        self.task_text = the_list_item.text


class ListItem(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

    def play(self, the_list_item):
        self.IconLeftWidget.icon = "pause" if self.IconLeftWidget.icon == "play" else "play"


if __name__ == '__main__':
    app = MainApp()
    app.run()