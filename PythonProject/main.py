import json
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle

# =============================================================================
# File Paths
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_image_path(image_path):
    return os.path.join(BASE_DIR, image_path)

# =============================================================================
# WINDOW
# =============================================================================

Window.clearcolor = (0.98, 0.97, 0.95, 1)


# =============================================================================
# COLOUR PALETTE
# =============================================================================

CREAM = (0.98, 0.97, 0.95, 1)
PARCHMENT = (0.96, 0.94, 0.91, 1)
INK = (0.11, 0.10, 0.09, 1)
SIENNA = (0.55, 0.29, 0.18, 1)
RUST = (0.75, 0.38, 0.23, 1)
OCHRE = (0.69, 0.49, 0.23, 1)
STONE = (0.48, 0.45, 0.41, 1)
DIVIDER = (0.85, 0.82, 0.77, 1)

# =============================================================================
# LOAD RECIPES
# =============================================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECIPE_FILE = os.path.join(BASE_DIR, "recipes.json")


def load_recipes():
    try:
        with open(RECIPE_FILE, "r", encoding="utf-8") as file:
            recipes = json.load(file)

        return recipes

    except FileNotFoundError:
        print("ERROR: recipes.json was not found.")
        return []

    except json.JSONDecodeError as error:
        print("ERROR: recipes.json contains invalid JSON.")
        print(error)
        return []

# =============================================================================
# DIVIDER
# =============================================================================

class Divider(Widget):

    def __init__(self, **kwargs):
        super().__init__(
            size_hint_y=None,
            height=dp(1),
            **kwargs
        )

        self.bind(
            pos=self.draw,
            size=self.draw
        )

    def draw(self, *_):
        self.canvas.clear()

        with self.canvas:
            Color(*DIVIDER)
            Rectangle(
                pos=self.pos,
                size=self.size
            )


# =============================================================================
# META ITEM
# =============================================================================

class MetaItem(BoxLayout):

    def __init__(self, label, value, **kwargs):

        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(52),
            **kwargs
        )

        title = Label(
            text=label.upper(),
            font_size=sp(10),
            bold=True,
            color=OCHRE,
            size_hint_y=None,
            height=dp(16),
            halign="left",
            valign="middle",
        )

        value_label = Label(
            text=value,
            font_size=sp(12),
            color=INK,
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle",
        )

        for label_widget in (title, value_label):
            label_widget.bind(
                size=lambda widget, _: setattr(
                    widget,
                    "text_size",
                    (widget.width, None)
                )
            )

        self.add_widget(title)
        self.add_widget(value_label)


# =============================================================================
# RECIPE CARD - MOBILE
# =============================================================================

class RecipeCard(RecycleDataViewBehavior, BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(260),
            padding=dp(0),
            spacing=dp(0),
            **kwargs
        )

        self.recipe = None
        self.rv = None

        # ---------------------------------------------------------
        # Card background
        # ---------------------------------------------------------

        with self.canvas.before:

            Color(*PARCHMENT)

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

        # ---------------------------------------------------------
        # Image
        # ---------------------------------------------------------

        self.image = AsyncImage(
            source="",

            allow_stretch=True,
            keep_ratio=True,

            size_hint_y=None,
            height=dp(145),
        )

        self.add_widget(
            self.image
        )

        # ---------------------------------------------------------
        # Text area
        # ---------------------------------------------------------

        self.text_area = BoxLayout(
            orientation="vertical",

            size_hint_y=None,
            height=dp(115),

            padding=(
                dp(14),
                dp(8),
                dp(14),
                dp(8)
            ),

            spacing=dp(1),
        )

        # ---------------------------------------------------------
        # Category
        # ---------------------------------------------------------

        self.category_label = Label(
            text="",

            font_size=sp(9),
            bold=True,

            color=OCHRE,

            size_hint_y=None,
            height=dp(15),

            halign="left",
            valign="middle",

            text_size=(None, None),
        )

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        self.title_label = Label(
            text="",

            font_size=sp(17),
            bold=True,

            color=INK,

            size_hint_y=None,

            height=dp(24),

            halign="left",
            valign="middle",

            shorten=True,
            shorten_from="right",
        )

        # ---------------------------------------------------------
        # Subtitle
        # ---------------------------------------------------------

        self.subtitle_label = Label(
            text="",

            font_size=sp(11),
            italic=True,

            color=STONE,

            size_hint_y=None,

            height=dp(28),

            halign="left",
            valign="top",

            shorten=True,
            shorten_from="right",
        )

        # ---------------------------------------------------------
        # Meta
        # ---------------------------------------------------------

        self.meta_label = Label(
            text="",

            font_size=sp(10),

            color=STONE,

            size_hint_y=None,
            height=dp(20),

            halign="left",
            valign="middle",

            shorten=True,
            shorten_from="right",
        )

        self.text_area.add_widget(
            self.category_label
        )

        self.text_area.add_widget(
            self.title_label
        )

        self.text_area.add_widget(
            self.subtitle_label
        )

        self.text_area.add_widget(
            Widget()
        )

        self.text_area.add_widget(
            self.meta_label
        )

        self.add_widget(
            self.text_area
        )

    # ---------------------------------------------------------
    # Background
    # ---------------------------------------------------------

    def update_background(self, *_):

        self.bg.pos = self.pos
        self.bg.size = self.size

    # ---------------------------------------------------------
    # Recipe data
    # ---------------------------------------------------------

    def refresh_view_attrs(
        self,
        rv,
        index,
        data
    ):

        changed = super().refresh_view_attrs(
            rv,
            index,
            data
        )

        self.rv = rv
        self.recipe = data.get("recipe")

        if not hasattr(self, "image"):
            return changed

        if self.recipe:

            self.image.source = get_image_path(
                self.recipe["image"]
            )

            self.category_label.text = (
                self.recipe["category"].upper()
            )

            self.title_label.text = (
                self.recipe["title"]
            )

            self.subtitle_label.text = (
                self.recipe["subtitle"]
            )

            self.meta_label.text = (
                f"{self.recipe['prep_time']} prep  •  "
                f"{self.recipe['cook_time']} cook  •  "
                f"Serves {self.recipe['serves']}"
            )

        return changed

    # ---------------------------------------------------------
    # Touch
    # ---------------------------------------------------------

    def on_touch_up(self, touch):

        if self.collide_point(*touch.pos):

            if self.recipe and self.rv:

                self.rv.parent_screen.on_recipe_selected(
                    self.recipe
                )

                return True

        return super().on_touch_up(touch)


# =============================================================================
# RECIPE RECYCLE VIEW - MOBILE
# =============================================================================

class RecipeRecycleView(RecycleView):

    def __init__(
        self,
        parent_screen,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.parent_screen = parent_screen

        layout = RecycleBoxLayout(

            orientation="vertical",

            default_size=(
                None,
                dp(260)
            ),

            default_size_hint=(
                1,
                None
            ),

            size_hint_y=None,

            padding=(
                dp(12),
                dp(12),
                dp(12),
                dp(20)
            ),

            spacing=dp(12),
        )

        layout.bind(
            minimum_height=layout.setter(
                "height"
            )
        )

        self.add_widget(
            layout
        )

        self.layout_manager = layout

        self.viewclass = RecipeCard

    def set_recipes(self, recipes):

        self.data = [
            {
                "recipe": recipe
            }

            for recipe in recipes
        ]


# =============================================================================
# RECIPE LIST SCREEN
# =============================================================================

class RecipeListScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.all_recipes = load_recipes()

        self.build_ui()

    # -------------------------------------------------------------------------
    # BUILD UI
    # -------------------------------------------------------------------------

    def build_ui(self):

        root = BoxLayout(
            orientation="vertical"
        )

        # =====================================================================
        # HEADER
        # =====================================================================

        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(125),

            padding=(
                dp(16),
                dp(10),
                dp(16),
                dp(8)
            ),

            spacing=dp(1),
        )

        # Header background
        with header.canvas.before:

            Color(*CREAM)

            header_bg = Rectangle(
                pos=header.pos,
                size=header.size
            )

        header.bind(
            pos=lambda widget, _: setattr(
                header_bg,
                "pos",
                widget.pos
            ),

            size=lambda widget, _: setattr(
                header_bg,
                "size",
                widget.size
            ),
        )

        # Small heading
        small_title = Label(
            text="A COLLECTION OF JACK'S RECIPES",
            font_size=sp(9),
            bold=True,
            color=OCHRE,
            size_hint_y=None,
            height=dp(16),
            halign="left",
            valign="middle",
        )

        # Main heading
        main_title = Label(
            text="Jack's Kitchen",
            font_size=sp(25),
            bold=True,
            color=INK,
            size_hint_y=None,
            height=dp(34),
            halign="left",
            valign="middle",
        )

        # Subtitle
        subtitle = Label(
            text="Good food made with care.",
            font_size=sp(12),
            italic=True,
            color=STONE,
            size_hint_y=None,
            height=dp(20),
            halign="left",
            valign="middle",
        )

        header.add_widget(small_title)
        header.add_widget(main_title)
        header.add_widget(subtitle)

        # Search box
        self.search = TextInput(
            hint_text="Search recipes...",

            size_hint_y=None,
            height=dp(44),

            font_size=sp(14),

            foreground_color=INK,

            hint_text_color=(
                *STONE[:3],
                0.7
            ),

            background_color=(
                *PARCHMENT[:3],
                1
            ),

            cursor_color=SIENNA,

            multiline=False,

            padding=(
                dp(12),
                dp(11)
            ),
        )

        self.search.bind(
            text=self.on_search
        )

        header.add_widget(
            self.search
        )

        root.add_widget(
            header
        )

        root.add_widget(
            Divider()
        )

        # =====================================================================
        # RECYCLE VIEW
        # =====================================================================

        self.recipe_view = RecipeRecycleView(
            parent_screen=self
        )

        root.add_widget(
            self.recipe_view
        )

        self.add_widget(
            root
        )

        # Populate
        self.populate(
            self.all_recipes
        )

    # -------------------------------------------------------------------------
    # SEARCH
    # -------------------------------------------------------------------------

    def on_search(self, instance, text):

        query = text.strip().lower()

        if not query:

            results = self.all_recipes

        else:

            results = [
                recipe

                for recipe in self.all_recipes

                if (
                    query in recipe["title"].lower()

                    or

                    query in recipe["category"].lower()

                    or

                    query in recipe["subtitle"].lower()
                )
            ]

        self.populate(results)

    # -------------------------------------------------------------------------
    # POPULATE
    # -------------------------------------------------------------------------

    def populate(self, recipes):

        self.recipe_view.set_recipes(
            recipes
        )

    # -------------------------------------------------------------------------
    # RECIPE SELECTED
    # -------------------------------------------------------------------------

    def on_recipe_selected(self, recipe):

        app = App.get_running_app()

        app.root.transition = SlideTransition(
            direction="left"
        )

        detail_screen = app.root.get_screen(
            "detail"
        )

        detail_screen.load_recipe(
            recipe
        )

        app.root.current = "detail"


# =============================================================================
# RECIPE DETAIL SCREEN
# =============================================================================

class RecipeDetailScreen(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.root_layout = BoxLayout(
            orientation="vertical"
        )

        self.add_widget(
            self.root_layout
        )

    # -------------------------------------------------------------------------
    # LOAD RECIPE
    # -------------------------------------------------------------------------


    def load_recipe(self, recipe):

        self.root_layout.clear_widgets()

        # =====================================================================
        # TOP BAR
        # =====================================================================

        topbar = BoxLayout(
            size_hint_y=None,
            height=dp(56),

            padding=(
                dp(8),
                dp(6),
                dp(8),
                dp(6)
            ),

            spacing=dp(6),
        )

        with topbar.canvas.before:

            Color(*PARCHMENT)

            tb_bg = Rectangle(
                pos=topbar.pos,
                size=topbar.size
            )

        topbar.bind(
            pos=lambda widget, _: setattr(
                tb_bg,
                "pos",
                widget.pos
            ),

            size=lambda widget, _: setattr(
                tb_bg,
                "size",
                widget.size
            ),
        )

        # Back button
        back_btn = Button(
            text="‹  Recipes",

            size_hint=(None, None),

            width=dp(105),
            height=dp(44),

            font_size=sp(14),

            background_normal="",

            background_color=(
                0,
                0,
                0,
                0
            ),

            color=SIENNA,

            bold=True,
        )

        back_btn.bind(
            on_release=self.go_back
        )

        topbar.add_widget(
            back_btn
        )

        topbar.add_widget(
            Widget()
        )

        # Category
        category_lbl = Label(
            text=recipe["category"].upper(),

            font_size=sp(9),

            bold=True,

            color=OCHRE,

            size_hint=(None, None),

            width=dp(80),
            height=dp(44),

            halign="right",
            valign="middle",
        )

        category_lbl.bind(
            size=lambda widget, _: setattr(
                widget,
                "text_size",
                (widget.width, None)
            )
        )

        topbar.add_widget(
            category_lbl
        )

        self.root_layout.add_widget(
            topbar
        )

        self.root_layout.add_widget(
            Divider()
        )

        # =====================================================================
        # SCROLLABLE BODY
        # =====================================================================

        scroll = ScrollView(
            bar_width=dp(4),
            bar_color=(
                *DIVIDER[:3],
                1
            )
        )

        body = BoxLayout(
            orientation="vertical",

            size_hint_y=None,

            padding=(
                dp(16),
                dp(14),
                dp(16),
                dp(30)
            ),

            spacing=dp(0),
        )

        body.bind(
            minimum_height=body.setter(
                "height"
            )
        )

        # =====================================================================
        # HERO IMAGE - RESPONSIVE 4:3
        # =====================================================================

        img = AsyncImage(
            source=get_image_path(recipe["image"]),

            allow_stretch=True,
            keep_ratio=True,

            size_hint_x=1,
            size_hint_y=None,

            height=dp(200),
        )

        def update_image_height(widget, *_):

            if widget.width > 0:
                # Maintain 4:3 aspect ratio
                widget.height = widget.width * 0.75

        img.bind(
            width=update_image_height
        )

        body.add_widget(
            img
        )

        # =====================================================================
        # TITLE
        # =====================================================================

        title = Label(
            text=recipe["title"],

            font_size=sp(24),

            bold=True,

            color=INK,

            size_hint_y=None,

            halign="left",
            valign="top",
        )

        title.bind(
            width=lambda widget, _: setattr(
                widget,
                "text_size",
                (widget.width, None)
            ),

            texture_size=lambda widget, _: setattr(
                widget,
                "height",
                widget.texture_size[1]
            ),
        )

        body.add_widget(
            title
        )

        # =====================================================================
        # SUBTITLE
        # =====================================================================

        subtitle = Label(
            text=recipe["subtitle"],

            font_size=sp(13),

            italic=True,

            color=STONE,

            size_hint_y=None,

            halign="left",
            valign="top",
        )

        subtitle.bind(
            width=lambda widget, _: setattr(
                widget,
                "text_size",
                (widget.width, None)
            ),

            texture_size=lambda widget, _: setattr(
                widget,
                "height",
                widget.texture_size[1]
            ),
        )

        body.add_widget(
            subtitle
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(14)
            )
        )

        body.add_widget(
            Divider()
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(12)
            )
        )

        # =====================================================================
        # META INFORMATION
        # =====================================================================

        meta_container = BoxLayout(
            orientation="vertical",

            size_hint_y=None,

            height=dp(108),

            spacing=dp(4),
        )

        meta_row_1 = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            spacing=dp(16),
        )

        meta_row_2 = BoxLayout(
            size_hint_y=None,
            height=dp(52),
            spacing=dp(16),
        )

        meta_items = [
            ("Prep", recipe["prep_time"]),
            ("Cook", recipe["cook_time"]),
            ("Serves", str(recipe["serves"])),
            ("Difficulty", recipe["difficulty"]),
        ]

        meta_row_1.add_widget(
            MetaItem(
                *meta_items[0]
            )
        )

        meta_row_1.add_widget(
            MetaItem(
                *meta_items[1]
            )
        )

        meta_row_2.add_widget(
            MetaItem(
                *meta_items[2]
            )
        )

        meta_row_2.add_widget(
            MetaItem(
                *meta_items[3]
            )
        )

        meta_container.add_widget(
            meta_row_1
        )

        meta_container.add_widget(
            meta_row_2
        )

        body.add_widget(
            meta_container
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(12)
            )
        )

        body.add_widget(
            Divider()
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(16)
            )
        )

        # =====================================================================
        # INTRO
        # =====================================================================

        intro_lbl = Label(
            text=recipe["intro"],

            font_size=sp(13),

            italic=True,

            color=INK,

            size_hint_y=None,

            halign="left",
            valign="top",
        )

        intro_lbl.bind(
            width=lambda widget, _: setattr(
                widget,
                "text_size",
                (widget.width, None)
            ),

            texture_size=lambda widget, _: setattr(
                widget,
                "height",
                widget.texture_size[1] + dp(4)
            ),
        )

        body.add_widget(
            intro_lbl
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(20)
            )
        )

        # =====================================================================
        # INGREDIENTS HEADING
        # =====================================================================

        body.add_widget(
            Label(
                text="Ingredients",

                font_size=sp(18),

                bold=True,

                color=SIENNA,

                size_hint_y=None,

                height=dp(30),

                halign="left",
            )
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(8)
            )
        )

        # =====================================================================
        # INGREDIENTS
        # =====================================================================

        for ingredient in recipe["ingredients"]:

            amount = ingredient["amount"]
            item = ingredient["item"]

            row = BoxLayout(
                size_hint_y=None,

                spacing=dp(10),

                padding=(
                    0,
                    dp(5),
                    0,
                    dp(5)
                ),
            )

            amount_lbl = Label(
                text=amount,

                font_size=sp(11),

                bold=True,

                color=OCHRE,

                size_hint_x=None,

                width=dp(65),

                size_hint_y=None,

                height=dp(24),

                halign="right",

                valign="middle",

                text_size=(
                    dp(65),
                    None
                ),
            )

            row.add_widget(
                amount_lbl
            )

            ingredient_lbl = Label(
                text=item,

                font_size=sp(13),

                color=INK,

                size_hint_y=None,

                halign="left",

                valign="top",
            )

            ingredient_lbl.bind(
                width=lambda widget, _: setattr(
                    widget,
                    "text_size",
                    (widget.width, None)
                ),

                texture_size=lambda widget, _: setattr(
                    widget,
                    "height",
                    max(
                        dp(24),
                        widget.texture_size[1]
                    )
                ),
            )

            row.add_widget(
                ingredient_lbl
            )

            row.bind(
                minimum_height=row.setter(
                    "height"
                )
            )

            body.add_widget(
                row
            )

            body.add_widget(
                Divider()
            )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(20)
            )
        )

        # =====================================================================
        # METHOD HEADING
        # =====================================================================

        body.add_widget(
            Label(
                text="Method",

                font_size=sp(18),

                bold=True,

                color=SIENNA,

                size_hint_y=None,

                height=dp(30),

                halign="left",
            )
        )

        body.add_widget(
            Widget(
                size_hint_y=None,
                height=dp(8)
            )
        )

        # =====================================================================
        # METHOD STEPS
        # =====================================================================

        for i, step in enumerate(
            recipe["steps"],
            1
        ):

            step_row = BoxLayout(
                size_hint_y=None,

                spacing=dp(12),

                padding=(
                    0,
                    dp(5),
                    0,
                    dp(10)
                ),
            )

            # Number
            num_lbl = Label(
                text=str(i),

                font_size=sp(11),

                bold=True,

                color=SIENNA,

                size_hint=(
                    None,
                    None
                ),

                width=dp(34),

                height=dp(34),

                halign="center",

                valign="middle",
            )

            with num_lbl.canvas.before:

                Color(*PARCHMENT)

                RoundedRectangle(
                    pos=num_lbl.pos,
                    size=(
                        dp(34),
                        dp(34)
                    ),
                    radius=[dp(17)]
                )

            step_row.add_widget(
                num_lbl
            )

            # Step text
            step_lbl = Label(
                text=step,

                font_size=sp(13),

                color=INK,

                size_hint_y=None,

                halign="left",

                valign="top",
            )

            step_lbl.bind(
                width=lambda widget, _: setattr(
                    widget,
                    "text_size",
                    (widget.width, None)
                ),

                texture_size=lambda widget, _: setattr(
                    widget,
                    "height",
                    widget.texture_size[1]
                ),
            )

            step_row.add_widget(
                step_lbl
            )

            step_row.bind(
                minimum_height=step_row.setter(
                    "height"
                )
            )

            body.add_widget(
                step_row
            )

        # =====================================================================
        # COOK'S NOTE
        # =====================================================================

        if recipe.get("note"):

            body.add_widget(
                Widget(
                    size_hint_y=None,
                    height=dp(16)
                )
            )

            note_box = BoxLayout(
                orientation="vertical",

                size_hint_y=None,

                padding=(
                    dp(14),
                    dp(12),
                    dp(14),
                    dp(12)
                ),
            )

            with note_box.canvas.before:

                Color(*PARCHMENT)

                note_box_bg = Rectangle(
                    pos=note_box.pos,
                    size=note_box.size
                )

                Color(*OCHRE)

                note_box_bar = Rectangle(
                    pos=note_box.pos,
                    size=(
                        dp(3),
                        note_box.height
                    )
                )

            note_box.bind(
                pos=lambda widget, _: (
                    setattr(
                        note_box_bg,
                        "pos",
                        widget.pos
                    ),
                    setattr(
                        note_box_bar,
                        "pos",
                        widget.pos
                    )
                ),

                size=lambda widget, _: (
                    setattr(
                        note_box_bg,
                        "size",
                        widget.size
                    ),
                    setattr(
                        note_box_bar,
                        "size",
                        (
                            dp(3),
                            widget.height
                        )
                    )
                ),
            )

            note_title = Label(
                text="COOK'S NOTE",

                font_size=sp(9),

                bold=True,

                color=OCHRE,

                size_hint_y=None,

                height=dp(16),

                halign="left",
            )

            note_box.add_widget(
                note_title
            )

            note_lbl = Label(
                text=recipe["note"],

                font_size=sp(12),

                italic=True,

                color=STONE,

                size_hint_y=None,

                halign="left",

                valign="top",
            )

            note_lbl.bind(
                width=lambda widget, _: setattr(
                    widget,
                    "text_size",
                    (widget.width, None)
                ),

                texture_size=lambda widget, _: setattr(
                    widget,
                    "height",
                    widget.texture_size[1] + dp(4)
                ),
            )

            note_box.add_widget(
                note_lbl
            )

            note_box.bind(
                minimum_height=note_box.setter(
                    "height"
                )
            )

            body.add_widget(
                note_box
            )

        # =====================================================================
        # ADD BODY
        # =====================================================================

        scroll.add_widget(
            body
        )

        self.root_layout.add_widget(
            scroll
        )

    # -------------------------------------------------------------------------
    # BACK
    # -------------------------------------------------------------------------

    def go_back(self, *_):

        app = App.get_running_app()

        app.root.transition = SlideTransition(
            direction="right"
        )

        app.root.current = "list"


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class CookbookApp(App):

    def build(self):

        screen_manager = ScreenManager()

        screen_manager.add_widget(
            RecipeListScreen(
                name="list"
            )
        )

        screen_manager.add_widget(
            RecipeDetailScreen(
                name="detail"
            )
        )

        return screen_manager


# =============================================================================
# RUN
# =============================================================================

if __name__ == "__main__":
    CookbookApp().run()