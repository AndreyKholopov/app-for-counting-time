from kivymd.app import MDApp

from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import TwoLineAvatarIconListItem

from time import sleep
from threading import Thread

from database import Database

db = Database()

class MainApp(MDApp):
    task_created_list_dialog = None
    task_changed_list_dialog = None
    tasks = []

    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"

    def show_task_dialog(self):
        if not self.task_created_list_dialog:
            self.task_created_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_created_list_dialog.open()

    def show_change_task_dialog(self, the_list_item):
        if not self.task_changed_list_dialog:
            self.task_changed_list_dialog = MDDialog(
                title="Change Task",
                type="custom",
                content_cls=DialogChangeContent(),
            )
  
        [hours, minutes] = the_list_item.secondary_text.split(':')
        self.task_changed_list_dialog.content_cls.ids.the_list_item = the_list_item
        self.task_changed_list_dialog.content_cls.ids.task_text.text = the_list_item.text
        self.task_changed_list_dialog.content_cls.ids.task_hours.text = hours
        self.task_changed_list_dialog.content_cls.ids.task_minutes.text = minutes

        self.task_changed_list_dialog.open()

    def close_dialog(self, *args):
        self.task_created_list_dialog.dismiss()

    def close_change_dialog(self, *args):
        self.task_changed_list_dialog.dismiss()
        
    def on_start(self):
        try:
            self.tasks = db.get_tasks()
            tasks = self.sort_list(self.tasks)
            self.render_list(tasks)

        except Exception as e:
            print(e)
            pass

    def filter_tasks(self, filter_by):
        self.root.ids.container.clear_widgets()
        tasks = self.sort_list(self.filter_list(self.tasks, filter_by))
        self.render_list(tasks)

    def filter_list(self, filtered_list, filter_by):
        def filter_name(item):
            res = str.__contains__(item[1], filter_by)
            return res

        res = list(filter(filter_name, filtered_list))      
        return res
    
    def sort_list(self, list):
        def takeFirst(elem):
            return elem[0]

        list.sort(key=takeFirst, reverse=True)
        return list

    def render_list(self, list):
        if list != []:
            for task in list:
                add_task = ListItem(pk=task[0], text=task[1], secondary_text=task[3]+':'+task[2])
                self.root.ids.container.add_widget(add_task)

    def add_task(self, task):
        created_task = db.create_task(task.text, 0, 0)

        self.root.ids.container.add_widget(ListItem(pk=created_task[0], text=created_task[1], secondary_text=created_task[3]+':'+created_task[2]), index=len(self.root.ids.container.children))

        task.text = ''

    def change_task(self, the_list_item, task_text, task_minutes, task_hours, *args):
        created_task = db.change_task(the_list_item.pk, task_text, task_minutes, task_hours)

        the_list_item.text=created_task[1]
        the_list_item.secondary_text=created_task[3]+':'+created_task[2]

        task_text = ''
        task_minutes = ''
        task_hours = ''


class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DialogChangeContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ListItem(TwoLineAvatarIconListItem):
    timer = None

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

    def play_or_pause(self, the_list_item, icon):
        if not self.timer or not self.timer.is_time_going:
            [hours, minutes] = the_list_item.secondary_text.split(':')
            self.timer = Timer(the_list_item, hours, minutes)
            th = Thread(target=Timer.start_timer, args=(self.timer, ))
            th.start()

            icon.icon = "pause"
            icon.text_color = [1, 0, 0, 1]
        else:
            [hours, minutes] = Timer.stop_timer(self.timer)

            icon.icon = "play"
            icon.text_color = [.5, .8, 0, 1]

            app.change_task(the_list_item, self.text, minutes, hours)


class Timer():
    is_time_going = 0
    change_task = None

    def __init__(self, the_list_item, hours, minutes, **kwargs):
        super().__init__(**kwargs)
        self.the_list_item = the_list_item
        self.hours = int(hours)
        self.minutes = int(minutes)
        self.seconds = 0

    def start_timer(self):
        self.is_time_going = 1
        while self.is_time_going:
            sleep(1)
            self.seconds += 1
            if self.seconds == 60:
                self.minutes += 1
                self.seconds = 0
                self.the_list_item.secondary_text=str(self.hours)+':'+str(self.minutes)
                if self.minutes == 60:
                    self.hours += 1
                    self.minutes = 0
                    self.the_list_item.secondary_text=str(self.hours)+':'+str(self.minutes)

    def stop_timer(self):
        self.is_time_going = 0
        return [self.hours, self.minutes]


if __name__ == '__main__':
    app = MainApp()
    app.run()