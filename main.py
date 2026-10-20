from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sqlite3

class SparePartsApp(App):
    def build(self):
        self.title = "إدارة المكائن وقطع الغيار"
        
        # إنشاء قاعدة البيانات المحلية
        self.conn = sqlite3.connect('factory_data.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # --- قسم إضافة مكينة جديدة ---
        root.add_widget(Label(text='--- إضافة مكينة جديدة ---', size_hint_y=None, height=30))
        self.machine_input = TextInput(hint_text='اسم المكينة (مثلاً: Omega 450)', multiline=False, size_hint_y=None, height=40)
        root.add_widget(self.machine_input)
        
        btn_add_machine = Button(text='حفظ المكينة', size_hint_y=None, height=45, background_color=(0.1, 0.6, 0.3, 1))
        btn_add_machine.bind(on_press=self.add_machine)
        root.add_widget(btn_add_machine)
        
        # --- قسم إضافة قطعة غيار ---
        root.add_widget(Label(text='--- إضافة قطعة غيار ---', size_hint_y=None, height=30))
        
        # قائمة منسدلة لاختيار المكينة
        self.machine_spinner = Spinner(text='اختر المكينة', values=self.get_machines_list(), size_hint_y=None, height=40)
        root.add_widget(self.machine_spinner)
        
        self.part_name_input = TextInput(hint_text='اسم القطعة (مثلاً: رومان بلي 6006)', multiline=False, size_hint_y=None, height=40)
        root.add_widget(self.part_name_input)
        
        self.specs_input = TextInput(hint_text='المواصفات والقياسات', multiline=False, size_hint_y=None, height=40)
        root.add_widget(self.specs_input)
        
        btn_add_part = Button(text='حفظ القطعة', size_hint_y=None, height=45, background_color=(0.2, 0.4, 0.8, 1))
        btn_add_part.bind(on_press=self.add_part)
        root.add_widget(btn_add_part)
        
        # --- قسم البحث ---
        root.add_widget(Label(text='--- البحث باسم المكينة ---', size_hint_y=None, height=30))
        self.search_input = TextInput(hint_text='اكتب اسم المكينة للبحث...', multiline=False, size_hint_y=None, height=40)
        self.search_input.bind(text=self.search_parts)
        root.add_widget(self.search_input)
        
        # شاشة لعرض النتائج
        self.results_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results_layout)
        root.add_widget(scroll)
        
        return root

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS machines (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS parts (id INTEGER PRIMARY KEY AUTOINCREMENT, machine_name TEXT, part_name TEXT, specs TEXT)''')
        self.conn.commit()

    def get_machines_list(self):
        try:
            self.cursor.execute("SELECT name FROM machines")
            rows = self.cursor.fetchall()
            return [row[0] for row in rows] if rows else ['لا توجد مكائن']
        except:
            return ['لا توجد مكائن']

    def add_machine(self, instance):
        name = self.machine_input.text.strip()
        if name:
            self.cursor.execute("INSERT INTO machines (name) VALUES (?)", (name,))
            self.conn.commit()
            self.machine_input.text = ''
            self.machine_spinner.values = self.get_machines_list()
            print("تمت إضافة المكينة بنجاح")

    def add_part(self, instance):
        machine = self.machine_spinner.text
        part_name = self.part_name_input.text.strip()
        specs = self.specs_input.text.strip()
        if machine and machine != 'اختر المكينة' and part_name:
            self.cursor.execute("INSERT INTO parts (machine_name, part_name, specs) VALUES (?, ?, ?)", (machine, part_name, specs))
            self.conn.commit()
            self.part_name_input.text = ''
            self.specs_input.text = ''
            print("تمت إضافة القطعة بنجاح")

    def search_parts(self, instance, query):
        self.results_layout.clear_widgets()
        if not query.strip():
            return
        self.cursor.execute("SELECT part_name, specs FROM parts WHERE machine_name LIKE ?", ('%' + query + '%',))
        rows = self.cursor.fetchall()
        for row in rows:
            lbl = Label(text=f"القطعة: {row[0]} | المواصفات: {row[1]}", size_hint_y=None, height=40)
            self.results_layout.add_widget(lbl)

if __name__ == '__main__':
    SparePartsApp().run()
