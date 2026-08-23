from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import AsyncImage
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle

Window.clearcolor = (0.98, 0.97, 0.95, 1)  # cream background

# -- Colour palette -----------------------------------------------------------------------
CREAM      = (0.98, 0.97, 0.95, 1)
PARCHMENT  = (0.96, 0.94, 0.91, 1)
INK        = (0.11, 0.10, 0.09, 1)
SIENNA     = (0.55, 0.29, 0.18, 1)
RUST       = (0.75, 0.38, 0.23, 1)
OCHRE      = (0.69, 0.49, 0.23, 1)
STONE      = (0.48, 0.45, 0.41, 1)
DIVIDER    = (0.85, 0.82, 0.77, 1)

# -- Recipe data -----------------------------------------------------------------------
RECIPES = [
    {
        "id": 1,
        "title": "Spaghetti al Pomodoro",
        "subtitle": "A slow-cooked tomato sauce with good olive oil and fresh basil",
        "category": "Pasta",
        "prep_time": "15 min",
        "cook_time": "45 min",
        "serves": 4,
        "difficulty": "Easy",
        "intro": (
            "The simplest things demand the most care. This sauce asks nothing of you "
            "except patience and good ingredients — San Marzano tomatoes, a generous "
            "pour of oil, and the discipline to leave it alone while it cooks."
        ),
        "image": "https://images.unsplash.com/photo-1484325881845-65073528922e?w=800&h=400&fit=crop&auto=format",
        "ingredients": [
            ("500 g", "spaghetti"),
            ("2 × 400 g", "tins whole San Marzano tomatoes"),
            ("5 tbsp", "extra-virgin olive oil, plus more to finish"),
            ("4 cloves", "garlic, peeled and lightly smashed"),
            ("1 small", "dried chilli, crumbled"),
            ("1 handful", "fresh basil leaves"),
            ("", "fine sea salt"),
        ],
        "steps": [
            "Warm the olive oil in a wide, heavy pan over medium-low heat. Add the garlic and chilli and cook gently for 5 minutes until faintly golden at the edges.",
            "Crush the tomatoes by hand into the pan. Season with salt. Raise the heat to a bubble, then lower to a gentle simmer.",
            "Cook uncovered for 35–40 minutes, stirring occasionally, until thick and glossy. Remove the garlic cloves.",
            "Bring a large pot of well-salted water to a boil. Cook spaghetti until just short of al dente.",
            "Lift the pasta into the sauce with tongs, adding a splash of pasta water. Toss over medium heat for 2 minutes. Finish with raw olive oil and torn basil.",
        ],
        "note": "A pinch of sugar and a strip of lemon zest added with the tomatoes will lift the sauce considerably.",
    },
    {
        "id": 2,
        "title": "Roast Chicken with Herbs",
        "subtitle": "Crisp-skinned, herb-buttered, rested properly",
        "category": "Poultry",
        "prep_time": "20 min",
        "cook_time": "1 hr 20 min",
        "serves": 4,
        "difficulty": "Moderate",
        "intro": (
            "Roast chicken separates confident cooks from anxious ones. No tricks — "
            "just dry skin, flavoured butter, high heat, and the discipline to let it rest."
        ),
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=800&h=400&fit=crop&auto=format",
        "ingredients": [
            ("1 × 1.8 kg", "free-range chicken, at room temperature"),
            ("80 g", "unsalted butter, softened"),
            ("4 sprigs", "fresh thyme, leaves picked"),
            ("2 sprigs", "fresh rosemary, finely chopped"),
            ("3 cloves", "garlic, minced"),
            ("1", "lemon, zested and halved"),
            ("2 tbsp", "olive oil"),
            ("", "flaky sea salt and black pepper"),
        ],
        "steps": [
            "Take the chicken from the refrigerator at least an hour before cooking. Preheat oven to 220 °C.",
            "Mix butter with thyme, rosemary, garlic, and lemon zest. Season well.",
            "Pat the chicken completely dry. Push two-thirds of the herb butter beneath the breast skin, rub the rest over the outside.",
            "Season the cavity, stuff with lemon halves. Drizzle with oil and finish with flaky salt.",
            "Roast for 20 minutes at 220 °C, then reduce to 180 °C for a further 55–60 minutes, basting twice.",
            "Rest loosely tented with foil for at least 20 minutes before carving.",
        ],
        "note": "Resting is not optional — it is when the juices redistribute. A properly rested bird will always be more succulent.",
    },
    {
        "id": 3,
        "title": "Country Sourdough",
        "subtitle": "An open-crumbed, naturally leavened loaf with a blistered crust",
        "category": "Bread",
        "prep_time": "30 min + 18 hr ferment",
        "cook_time": "50 min",
        "serves": 1,
        "difficulty": "Advanced",
        "intro": (
            "Bread is as old as civilisation, and this loaf will teach you something each "
            "time you bake it. The process spans two days, but the active work is minutes."
        ),
        "image": "https://images.unsplash.com/photo-1559811814-e2c57b5e69df?w=800&h=400&fit=crop&auto=format",
        "ingredients": [
            ("450 g", "strong white bread flour"),
            ("50 g", "whole wheat flour"),
            ("375 g", "water at 30 °C"),
            ("100 g", "active sourdough starter (100% hydration)"),
            ("10 g", "fine sea salt"),
        ],
        "steps": [
            "Autolyse: Mix flour and 325 g water until no dry flour remains. Cover and rest 45 minutes.",
            "Add starter and remaining water; mix. Rest 30 minutes, then add salt and mix again.",
            "Bulk fermentation: Over 4 hours perform 4 sets of coil folds at 30-minute intervals. Dough is ready when it has grown ~50% and feels airy.",
            "Pre-shape into a loose round. Rest uncovered 20–30 minutes, then final-shape and place seam-side-up in a floured banneton.",
            "Cover and refrigerate overnight, 10–14 hours.",
            "Preheat a Dutch oven at 250 °C for 1 hour. Score the cold dough and bake covered 20 minutes, then uncovered 25–30 minutes until deeply mahogany.",
            "Cool on a wire rack for at least 2 hours before slicing.",
        ],
        "note": "If your starter doesn't double within 4–8 hours of feeding, give it two or three more feedings before attempting this.",
    },
    {
        "id": 4,
        "title": "Spiced Lamb Shoulder",
        "subtitle": "Slow-roasted with cumin, coriander, and preserved lemon",
        "category": "Meat",
        "prep_time": "25 min",
        "cook_time": "4 hr",
        "serves": 6,
        "difficulty": "Easy",
        "intro": (
            "Lamb shoulder is unforgiving only if you rush it. Given time and low heat, "
            "the collagen dissolves, the fat renders, and you are left with meat that falls "
            "apart at the press of a spoon."
        ),
        "image": "https://images.unsplash.com/photo-1523813301608-f54a198f6b5f?w=800&h=400&fit=crop&auto=format",
        "ingredients": [
            ("1 × 2.2 kg", "bone-in lamb shoulder"),
            ("2 tsp", "ground cumin"),
            ("2 tsp", "ground coriander"),
            ("1 tsp", "smoked paprika"),
            ("½ tsp", "ground cinnamon"),
            ("2", "preserved lemon quarters, skin finely chopped"),
            ("4 cloves", "garlic, minced"),
            ("3 tbsp", "olive oil"),
            ("250 ml", "chicken stock or water"),
            ("", "sea salt and black pepper"),
        ],
        "steps": [
            "Make the spice paste: combine all spices, preserved lemon, garlic, and olive oil. Season generously.",
            "Score the lamb deeply all over. Massage the paste into every surface and into the cuts. Refrigerate overnight if possible.",
            "Bring lamb to room temperature 1 hour before cooking. Preheat oven to 220 °C. Place in a deep tray, pour in stock, roast uncovered 20 minutes.",
            "Cover tightly with double foil, reduce to 160 °C, and roast 3–3.5 hours until a skewer meets no resistance near the bone.",
            "Remove foil, raise to 200 °C, roast 15 minutes more to lacquer. Rest 30 minutes, then pull apart with forks.",
        ],
        "note": "The braising juices are extraordinary — skim off excess fat and serve them alongside as a sauce.",
    },
]
# -- repeat widgets ----------------------------------------------------------------

class Divider(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(1), **kwargs)
        self.bind(pos=self.draw, size=self.draw)

    def draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*DIVIDER)
            Rectangle(pos=self.pos, size=self.size)

# -- Screens -----------------------------------------------------------------------

class RecipeListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.all_recipes = RECIPES
        self.build_ui()

    def build_ui(self):
        root = BoxLayout(orientation="vertical")

        # --Header--
        header = BoxLayout(orientation="vertical",
                           size_hint_y=None,
                           height=dp(160),
                           padding=(dp(28), dp(20), dp(28), dp(12))
                           )

        with header.canvas.before:
            Color(*CREAM)
            self.header_bg = Rectangle(pos=header.pos,
                                       size=header.size)

        header.bind(pos=lambda w, _: setattr(self.header_bg, "pos", w.pos),
                    size=lambda w, _: setattr(self.header_bg, "size", w.size))

        header.add_widget(Label(text="A COLLECTION OF JACKS RECIPES",
                                font_size=dp(9),
                                bold=True,
                                color=OCHRE,
                                size_hint_y=None,
                                height=dp(16),
                                halign="left",
                                valign="middle",
                                ))
        header.add_widget(Label(text="Jacks Kitchen",
                                font_size=dp(34),
                                bold=True,
                                color=INK,
                                size_hint_y=None,
                                height=dp(46),
                                halign="left",
                                valign="middle",
                                ))
        header.add_widget(Label(text="Good food made with care.",
                                font_size=dp(13),
                                italic=True,
                                color=STONE,
                                size_hint_y=None,
                                height=dp(22),
                                halign="left",
                                valign="middle",
                                ))

        self.search = TextInput(hint_text="Search recipes or tags...",
                                size_hint_y=None,
                                height=dp(36),
                                font_size=dp(13),
                                foreground_color=INK,
                                hint_text_color=(*STONE[:3], 0.7),
                                background_color=(*PARCHMENT[:3], 1),
                                cursor_color=SIENNA,
                                multiline=False,
                                padding=(dp(10), dp(8)),
                                )
        self.search.bind(text=self.on_search)
        header.add_widget(self.search)

        for lbl in header.children:
            if isinstance(lbl, Label):
                lbl.bind(size=lambda w, _: setattr(w, "text_size", (w.width, None)))



        root.add_widget(header)
        root.add_widget(Divider())

        #-- scrollable card list --
        self.scroll = ScrollView(bar_width=dp(4), bar_color=(*DIVIDER[:3], 1))
        self.card_list = BoxLayout(orientation="vertical",
                                   size_hint_y=None,
                                   spacing=dp(1),
                                   padding=(dp(20), dp(16), dp(20), dp(20)),
                                   )
        self.card_list.bind(minimum_height=self.card_list.setter("height"))
        self.scroll.add_widget(self.card_list)
        root.add_widget(self.scroll)

        self.add_widget(root)
        self.populate(RECIPES)

    def on_search(self, instance, text):
        q = text.strip().lower()
        results = [
            r for r in self.all_recipes
            if q in r["title"].lower() or q in r["category"].lower()
        ] if q else self.all_recipes
        self.populate(results)

    def populate(self, recipes):
        self.card_list.clear_widgets()
        for recipe in recipes:
            self.card_list.add_widget(self.make_card(recipe))
            self.card_list.add_widget(Widget(size_hint_y=None, height=dp(12)))

    def make_card(self, recipe):
        card = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(260),
        )
        with card.canvas.before:
            Color(*PARCHMENT)
            card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[dp(4),])
        card.bind(
            pos=lambda w, _: setattr(w.bg, "pos", w.pos),
            size=lambda w, _: setattr(w.bg, "size", w.size),
        )

        # Image
        img = AsyncImage(
            source=recipe["image"],
            allow_stretch=True,
            keep_ratio=False,
            size_hint_y=None,
            height=dp(150),
        )
        card.add_widget(img)

        # Text area
        text_area = BoxLayout(
            orientation="vertical",
            padding=(dp(14), dp(10), dp(14), dp(10)),
            spacing=dp(4),
        )
        text_area.add_widget(Label(
            text=recipe["category"].upper(),
            font_size=dp(9),
            bold=True,
            color=OCHRE,
            size_hint_y=None,
            height=dp(14),
            halign="left",
        ))
        title_lbl = Label(
            text=recipe["title"],
            font_size=dp(16),
            bold=True,
            color=INK,
            size_hint_y=None,
            height=dp(22),
            halign="left",
        )
        text_area.add_widget(title_lbl)
        sub_lbl = Label(
            text=recipe["subtitle"],
            font_size=dp(11),
            italic=True,
            color=STONE,
            size_hint_y=None,
            height=dp(28),
            halign="left",
        )
        text_area.add_widget(sub_lbl)

        meta = Label(
            text=f"{recipe['prep_time']} prep  ·  {recipe['cook_time']} cook  ·  Serves {recipe['serves']}",
            font_size=dp(10),
            color=STONE,
            size_hint_y=None,
            height=dp(16),
            halign="left",
        )
        text_area.add_widget(meta)

        for w in text_area.children:
            if isinstance(w, Label):
                w.bind(size=lambda lbl, _: setattr(lbl, "text_size", (lbl.width, None)))

        card.add_widget(text_area)
        return card







class CookbookApp(App):
    def build(self):
        return RecipeListScreen()

if __name__ == "__main__":
    CookbookApp().run()