"""
HSC English Prescribed Texts data and constraint logic.
Source: NESA HSC English Prescriptions 2027–2030 (D2025/464194)
"""

from dataclasses import dataclass, field
from itertools import product, combinations
from typing import Optional


@dataclass(frozen=True)
class Text:
    author: str
    title: str
    text_type: str  # "Prose fiction", "Poetry", "Drama", "Nonfiction", "Film", "Media", etc.
    text_type_category: str  # The broad category for constraint checking
    course: str
    focus_area: str
    paired_with: Optional[str] = None  # For Textual Conversations
    selections: str = ""
    is_shakespeare: bool = False


@dataclass
class TextPair:
    """A Textual Conversations pair (two texts studied together)."""
    text_a: Text
    text_b: Text
    label: str  # e.g. "Baynton + Cobby Eckermann"
    category: str  # e.g. "Prose fiction and poetry"

    @property
    def text_types(self) -> set[str]:
        return {self.text_a.text_type_category, self.text_b.text_type_category}

    @property
    def has_shakespeare(self) -> bool:
        return self.text_a.is_shakespeare or self.text_b.is_shakespeare


# =============================================================================
# TEXT TYPE CATEGORIES (for constraint checking)
# =============================================================================
# The 4th prescribed text must come from: drama OR nonfiction OR film OR media
# The constraint is: across all 4 texts, you need prose fiction, poetry,
# and one from {drama, nonfiction, film, media}.
# Since Textual Conversations gives you TWO texts, plus Critical Study gives ONE,
# plus Texts & Human Experiences gives ONE = 4 total.
# But the "4 prescribed texts" for Advanced are:
#   - 1 from Texts and human experiences
#   - 2 from Textual conversations (the pair)
#   - 1 from Critical study of literature
# Across these 4, you need: prose fiction, poetry, and drama/nonfiction/film/media.
# At least one must be Shakespeare.

CAT_PROSE = "Prose fiction"
CAT_POETRY = "Poetry"
CAT_DRAMA = "Drama"
CAT_NONFICTION = "Nonfiction"
CAT_FILM = "Film"
CAT_SHAKESPEARE = "Drama, Shakespearean text"

# For constraint purposes, Shakespeare drama counts as "Drama"
def broad_category(cat: str) -> str:
    if cat == CAT_SHAKESPEARE:
        return CAT_DRAMA
    return cat

REQUIRED_CATEGORIES = {CAT_PROSE, CAT_POETRY}
# Plus at least one from the "other" group:
OTHER_CATEGORIES = {CAT_DRAMA, CAT_NONFICTION, CAT_FILM, "Media"}


# =============================================================================
# ADVANCED TEXTS
# =============================================================================

# --- Texts and human experiences (Standard & Advanced share these) ---
ADVANCED_COMMON = [
    Text("Au, Jessica", "Cold Enough for Snow", "Prose fiction", CAT_PROSE,
         "Advanced", "Texts and human experiences"),
    Text("Malouf, David", "An Imaginary Life", "Prose fiction", CAT_PROSE,
         "Advanced", "Texts and human experiences"),
    Text("Lawson, Henry", "The Penguin Henry Lawson Short Stories", "Prose fiction", CAT_PROSE,
         "Advanced", "Texts and human experiences",
         selections="'The Drover's Wife', 'The Union Buries Its Dead', 'Shooting the Moon', 'Our Pipes', 'The Loaded Dog'"),
    Text("Dobson, Rosemary", "Selected poems of Rosemary Dobson", "Poetry", CAT_POETRY,
         "Advanced", "Texts and human experiences",
         selections="'Young Girl at a Window', 'Summer's End', 'Cock Crow', 'A Fine Thing', 'Child of Our Time', 'Piltdown Man', 'Every Man His Own Sculptor'"),
    Text("Harwood, Gwen", "Selected Poems", "Poetry", CAT_POETRY,
         "Advanced", "Texts and human experiences",
         selections="'The Glass Jar', 'The Violets', 'At Mornington', 'Father and Child, I and II', 'A Valediction', 'Beyond Metaphor', 'The Sharpness of Death'"),
    Text("Watson, Samuel Wagan", "Love Poems and Death Threats", "Poetry", CAT_POETRY,
         "Advanced", "Texts and human experiences",
         selections="'The Remedy of Butterflies', 'Finn', 'Let's Talk!', 'El Diablo Highway', 'Blacktracker... Blackwriter... Blacksubject', 'End of Days', 'Addendum'"),
    Text("Flanagan, Richard", "Question 7", "Nonfiction", CAT_NONFICTION,
         "Advanced", "Texts and human experiences"),
    Text("Gow, Michael", "Away", "Drama", CAT_DRAMA,
         "Advanced", "Texts and human experiences"),
    Text("Perkins, Rachel", "One Night the Moon", "Film", CAT_FILM,
         "Advanced", "Texts and human experiences"),
]

# --- Textual conversations (PAIRS) ---
_tc_baynton = Text("Baynton, Barbara", "Bush Studies", "Prose fiction", CAT_PROSE,
                    "Advanced", "Textual conversations")
_tc_cobby = Text("Cobby Eckermann, Ali", "Inside My Mother", "Poetry", CAT_POETRY,
                 "Advanced", "Textual conversations",
                 selections="'Clay', 'Inside My Mother', 'Warriors at Salt Creek', 'Unearth', 'Eyes', 'Key', 'Jacob', 'Nurture'")

_tc_blake = Text("Blake, William", "The Complete Poems", "Poetry", CAT_POETRY,
                 "Advanced", "Textual conversations",
                 selections="'To Morning'; (Songs of Experience) 'The Sick Rose', 'The Tyger', 'The Human Abstract', 'A Poison Tree'; 'Proverbs of Hell' (Plates 7-11), 'The [First] Book of Urizen, Chap: 1' (Plate 3)")
_tc_tokarczuk = Text("Tokarczuk, Olga", "Drive Your Plow Over the Bones of the Dead", "Prose fiction", CAT_PROSE,
                     "Advanced", "Textual conversations")

_tc_keats = Text("Keats, John", "The Complete Poems", "Poetry", CAT_POETRY,
                 "Advanced", "Textual conversations",
                 selections="'On First Looking into Chapman's Homer', 'When I have fears…', 'La Belle Dame sans Merci', 'Ode on a Grecian Urn', 'Ode to a Nightingale', 'Ode on Melancholy', 'Bright star!…'")
_tc_campion = Text("Campion, Jane", "Bright Star", "Film", CAT_FILM,
                   "Advanced", "Textual conversations")

_tc_hamlet = Text("Shakespeare, William", "Hamlet", "Drama, Shakespearean text", CAT_SHAKESPEARE,
                  "Advanced", "Textual conversations", is_shakespeare=True)
_tc_dickinson = Text("Dickinson, Emily", "The Complete Poems", "Poetry", CAT_POETRY,
                     "Advanced", "Textual conversations",
                     selections="167 ('To learn the Transport by the Pain'), 280 ('I felt a Funeral, in my Brain'), 384 ('No Rack can torture me'), 435 ('Much Madness is divinest Sense'), 449 ('I died for Beauty — but was scarce'), 670 ('One need not be a Chamber — to be Haunted'), 712 ('Because I could not stop for Death'), 149 ('A little East of Jordan')")

_tc_julius = Text("Shakespeare, William", "Julius Caesar", "Drama, Shakespearean text", CAT_SHAKESPEARE,
                  "Advanced", "Textual conversations", is_shakespeare=True)
_tc_machiavelli = Text("Machiavelli, Niccolo", "The Prince", "Nonfiction", CAT_NONFICTION,
                       "Advanced", "Textual conversations")

_tc_woolf = Text("Woolf, Virginia", "Mrs Dalloway", "Prose fiction", CAT_PROSE,
                 "Advanced", "Textual conversations")
_tc_daldry = Text("Daldry, Stephen", "The Hours", "Film", CAT_FILM,
                  "Advanced", "Textual conversations")

ADVANCED_TC_PAIRS = [
    TextPair(_tc_baynton, _tc_cobby,
             "Baynton + Cobby Eckermann", "Prose fiction and poetry"),
    TextPair(_tc_blake, _tc_tokarczuk,
             "Blake + Tokarczuk", "Poetry and prose fiction"),
    TextPair(_tc_keats, _tc_campion,
             "Keats + Campion", "Poetry and film"),
    TextPair(_tc_hamlet, _tc_dickinson,
             "Shakespeare + Dickinson", "Drama and poetry"),
    TextPair(_tc_julius, _tc_machiavelli,
             "Shakespeare + Machiavelli", "Drama and nonfiction"),
    TextPair(_tc_woolf, _tc_daldry,
             "Woolf + Daldry", "Prose fiction and film"),
]

# --- Critical study of literature ---
ADVANCED_CRIT = [
    Text("Austen, Jane", "Pride and Prejudice", "Prose fiction", CAT_PROSE,
         "Advanced", "Critical study of literature"),
    Text("Ondaatje, Michael", "Warlight", "Prose fiction", CAT_PROSE,
         "Advanced", "Critical study of literature"),
    Text("Glück, Louise", "Poems", "Poetry", CAT_POETRY,
         "Advanced", "Critical study of literature",
         selections="'The Wild Iris', 'Nostos', 'Vita Nova', 'Youth', 'Mitosis', 'Harvest', 'A Village Life'"),
    Text("Yeats, William Butler", "WB Yeats: Poems selected by Seamus Heaney", "Poetry", CAT_POETRY,
         "Advanced", "Critical study of literature",
         selections="'The Wild Swans at Coole', 'An Irish Airman…', 'Easter 1916', 'The Second Coming', 'Sailing to Byzantium', 'An Acre of Grass', 'Long-legged Fly'"),
    Text("Shakespeare, William", "Othello", "Drama, Shakespearean text", CAT_SHAKESPEARE,
         "Advanced", "Critical study of literature", is_shakespeare=True),
    Text("Shakespeare, William", "King Henry IV, Part 1", "Drama, Shakespearean text", CAT_SHAKESPEARE,
         "Advanced", "Critical study of literature", is_shakespeare=True),
]


# =============================================================================
# CONSTRAINT ENGINE
# =============================================================================

def get_all_type_categories(pair: TextPair, crit: Text, common: Text) -> list[str]:
    """Get the broad type categories for all 4 texts in a combination."""
    return [
        broad_category(pair.text_a.text_type_category),
        broad_category(pair.text_b.text_type_category),
        broad_category(crit.text_type_category),
        broad_category(common.text_type_category),
    ]


def has_shakespeare(pair: TextPair, crit: Text, common: Text) -> bool:
    return pair.has_shakespeare or crit.is_shakespeare or common.is_shakespeare


def is_valid_combination(pair: TextPair, crit: Text, common: Text) -> bool:
    """
    Check if a combination of (TC pair, Critical Study text, Common text) is valid.

    Rules for Advanced Year 12:
    1. Must include at least one prose fiction
    2. Must include at least one poetry
    3. Must include at least one from {drama, nonfiction, film, media}
    4. At least one text must be Shakespeare
    """
    cats = get_all_type_categories(pair, crit, common)
    cat_set = set(cats)

    has_prose = CAT_PROSE in cat_set
    has_poetry = CAT_POETRY in cat_set
    has_other = bool(cat_set & OTHER_CATEGORIES)
    has_shakes = has_shakespeare(pair, crit, common)

    return has_prose and has_poetry and has_other and has_shakes


def generate_all_valid_combinations() -> list[tuple[TextPair, Text, Text]]:
    """Generate all valid (pair, crit, common) combinations for Advanced."""
    valid = []
    for pair, crit, common in product(ADVANCED_TC_PAIRS, ADVANCED_CRIT, ADVANCED_COMMON):
        if is_valid_combination(pair, crit, common):
            valid.append((pair, crit, common))
    return valid


def get_compatible_texts(
    chosen_pair: Optional[TextPair] = None,
    chosen_crit: Optional[Text] = None,
    chosen_common: Optional[Text] = None,
) -> tuple[list[TextPair], list[Text], list[Text]]:
    """
    Given partial selections, return only the texts that can still
    lead to at least one valid combination.
    """
    valid_pairs = []
    valid_crits = []
    valid_commons = []

    for pair, crit, common in product(ADVANCED_TC_PAIRS, ADVANCED_CRIT, ADVANCED_COMMON):
        if chosen_pair and pair != chosen_pair:
            continue
        if chosen_crit and crit != chosen_crit:
            continue
        if chosen_common and common != chosen_common:
            continue
        if is_valid_combination(pair, crit, common):
            if pair not in valid_pairs:
                valid_pairs.append(pair)
            if crit not in valid_crits:
                valid_crits.append(crit)
            if common not in valid_commons:
                valid_commons.append(common)

    return valid_pairs, valid_crits, valid_commons


def is_selection_complete(
    chosen_pair: Optional[TextPair],
    chosen_crit: Optional[Text],
    chosen_common: Optional[Text],
) -> bool:
    return chosen_pair is not None and chosen_crit is not None and chosen_common is not None


def count_remaining_combinations(
    chosen_pair: Optional[TextPair] = None,
    chosen_crit: Optional[Text] = None,
    chosen_common: Optional[Text] = None,
) -> int:
    count = 0
    for pair, crit, common in product(ADVANCED_TC_PAIRS, ADVANCED_CRIT, ADVANCED_COMMON):
        if chosen_pair and pair != chosen_pair:
            continue
        if chosen_crit and crit != chosen_crit:
            continue
        if chosen_common and common != chosen_common:
            continue
        if is_valid_combination(pair, crit, common):
            count += 1
    return count


# =============================================================================
# STANDARD TEXTS
# =============================================================================

# --- Standard: Texts and human experiences (shared pool with Advanced) ---
STANDARD_COMMON = [
    Text("Au, Jessica", "Cold Enough for Snow", "Prose fiction", CAT_PROSE,
         "Standard", "Texts and human experiences"),
    Text("Malouf, David", "An Imaginary Life", "Prose fiction", CAT_PROSE,
         "Standard", "Texts and human experiences"),
    Text("Lawson, Henry", "The Penguin Henry Lawson Short Stories", "Prose fiction", CAT_PROSE,
         "Standard", "Texts and human experiences",
         selections="'The Drover's Wife', 'The Union Buries Its Dead', 'Shooting the Moon', 'Our Pipes', 'The Loaded Dog'"),
    Text("Dobson, Rosemary", "Selected poems of Rosemary Dobson", "Poetry", CAT_POETRY,
         "Standard", "Texts and human experiences",
         selections="'Young Girl at a Window', 'Summer's End', 'Cock Crow', 'A Fine Thing', 'Child of Our Time', 'Piltdown Man', 'Every Man His Own Sculptor'"),
    Text("Harwood, Gwen", "Selected Poems", "Poetry", CAT_POETRY,
         "Standard", "Texts and human experiences",
         selections="'The Glass Jar', 'The Violets', 'At Mornington', 'Father and Child, I and II', 'A Valediction', 'Beyond Metaphor', 'The Sharpness of Death'"),
    Text("Watson, Samuel Wagan", "Love Poems and Death Threats", "Poetry", CAT_POETRY,
         "Standard", "Texts and human experiences",
         selections="'The Remedy of Butterflies', 'Finn', 'Let's Talk!', 'El Diablo Highway', 'Blacktracker... Blackwriter... Blacksubject', 'End of Days', 'Addendum'"),
    Text("Flanagan, Richard", "Question 7", "Nonfiction", CAT_NONFICTION,
         "Standard", "Texts and human experiences"),
    Text("Gow, Michael", "Away", "Drama", CAT_DRAMA,
         "Standard", "Texts and human experiences"),
    Text("Perkins, Rachel", "One Night the Moon", "Film", CAT_FILM,
         "Standard", "Texts and human experiences"),
]

# --- Standard: Language, identity and culture ---
STANDARD_LIC = [
    Text("Lahiri, Jhumpa", "The Namesake", "Prose fiction", CAT_PROSE,
         "Standard", "Language, identity and culture"),
    Text("Winch, Tara June", "Swallow the Air", "Prose fiction", CAT_PROSE,
         "Standard", "Language, identity and culture"),
    Text("Antrobus, Raymond", "The Perseverance", "Poetry", CAT_POETRY,
         "Standard", "Language, identity and culture",
         selections="'Echo', 'Jamaican British', 'Ode to My Hair', 'Dear Hearing World', 'The Ghost of Laura Bridgman Warns Helen Keller About Fame', 'Dr Marigold Reevaluated', 'To Sweeten Bitter'"),
    Text("Aitken, Adam, Boey, Kim Cheng and Cahill, Michelle (eds)", "Contemporary Asian Australian Poets", "Poetry", CAT_POETRY,
         "Standard", "Language, identity and culture",
         selections="Boey, 'Stamp Collecting'; Khokhar, 'The Onyx Ring'; Wei Wei Lo, 'Bumboat Cruise on the Singapore River'; Musa, 'Air Force Ones'; Yu, 'New Accents'; Savige, 'Circular Breathing'; Ten, 'Translucent Jade'"),
    Text("Bairéad, Colm", "The Quiet Girl", "Film", CAT_FILM,
         "Standard", "Language, identity and culture"),
    Text("Valentine, Alana", "Shafana and Aunt Sarrinah", "Drama", CAT_DRAMA,
         "Standard", "Language, identity and culture"),
]

# --- Standard: Close study of literature ---
STANDARD_CLOSE = [
    Text("Anderson, MT", "Feed", "Prose fiction", CAT_PROSE,
         "Standard", "Close study of literature"),
    Text("Arnott, Robbie", "Limberlost", "Prose fiction", CAT_PROSE,
         "Standard", "Close study of literature"),
    Text("Duffy, Carol Ann", "Collected Poems", "Poetry", CAT_POETRY,
         "Standard", "Close study of literature",
         selections="'War Photographer', 'Stealing', 'In Mrs Tilscher's Class', 'We Remember Your Childhood Well', 'The Good Teachers', 'Little Red Cap', 'Mrs Midas'"),
    Text("Noonuccal, Oodgeroo", "My People", "Poetry", CAT_POETRY,
         "Standard", "Close study of literature",
         selections="'Corroboree', 'Ballad of the Totems', 'No More Boomerang', 'Son of Mine', 'We Are Going', 'The Past', 'Reed Flute Cave'"),
    Text("Shakespeare, William", "Much Ado About Nothing", "Drama", CAT_DRAMA,
         "Standard", "Close study of literature"),
    Text("Villeneuve, Denis", "Arrival", "Film", CAT_FILM,
         "Standard", "Close study of literature"),
]


# =============================================================================
# STANDARD CONSTRAINT ENGINE
# =============================================================================
# Standard Year 12: 3 prescribed texts, ONE per focus area.
# Must have one from each of: prose fiction, poetry, drama/film/media/nonfiction.
# NO Shakespeare requirement.

def is_valid_standard_combination(common: Text, lic: Text, close: Text) -> bool:
    """
    Check if a Standard combination is valid.
    Rules:
    1. Must include at least one prose fiction
    2. Must include at least one poetry
    3. Must include at least one from {drama, nonfiction, film, media}
    """
    cats = {
        broad_category(common.text_type_category),
        broad_category(lic.text_type_category),
        broad_category(close.text_type_category),
    }
    has_prose = CAT_PROSE in cats
    has_poetry = CAT_POETRY in cats
    has_other = bool(cats & OTHER_CATEGORIES)
    return has_prose and has_poetry and has_other


def generate_all_valid_standard_combinations() -> list[tuple[Text, Text, Text]]:
    """Generate all valid (common, lic, close) combinations for Standard."""
    valid = []
    for common, lic, close in product(STANDARD_COMMON, STANDARD_LIC, STANDARD_CLOSE):
        if is_valid_standard_combination(common, lic, close):
            valid.append((common, lic, close))
    return valid


def get_standard_compatible_texts(
    chosen_common: Optional[Text] = None,
    chosen_lic: Optional[Text] = None,
    chosen_close: Optional[Text] = None,
) -> tuple[list[Text], list[Text], list[Text]]:
    """
    Given partial selections, return only texts that can still
    lead to at least one valid Standard combination.
    """
    valid_commons = []
    valid_lics = []
    valid_closes = []

    for common, lic, close in product(STANDARD_COMMON, STANDARD_LIC, STANDARD_CLOSE):
        if chosen_common and common != chosen_common:
            continue
        if chosen_lic and lic != chosen_lic:
            continue
        if chosen_close and close != chosen_close:
            continue
        if is_valid_standard_combination(common, lic, close):
            if common not in valid_commons:
                valid_commons.append(common)
            if lic not in valid_lics:
                valid_lics.append(lic)
            if close not in valid_closes:
                valid_closes.append(close)

    return valid_commons, valid_lics, valid_closes


def count_remaining_standard(
    chosen_common: Optional[Text] = None,
    chosen_lic: Optional[Text] = None,
    chosen_close: Optional[Text] = None,
) -> int:
    count = 0
    for common, lic, close in product(STANDARD_COMMON, STANDARD_LIC, STANDARD_CLOSE):
        if chosen_common and common != chosen_common:
            continue
        if chosen_lic and lic != chosen_lic:
            continue
        if chosen_close and close != chosen_close:
            continue
        if is_valid_standard_combination(common, lic, close):
            count += 1
    return count


# =============================================================================
# EAL/D TEXTS
# =============================================================================

# --- EAL/D Focus Area 1: Texts and human experiences ---
EALD_FA1 = [
    Text("Parrett, Favel", "Past the Shallows", "Prose fiction", CAT_PROSE,
         "EAL/D", "Texts and human experiences"),
    Text("van Neerven, Ellen (ed)", "Flock: First Nations Stories Then and Now", "Prose fiction", CAT_PROSE,
         "EAL/D", "Texts and human experiences",
         selections="van Neerven, 'Each City'; Thompson, 'Honey'; Saward, 'Galah'; Saunders, 'River Story'; Lucashenko, 'Dreamers'; Leane, 'Forbidden Fruit'"),
    Text("Gray, Robert", "Coast Road: Selected Poems", "Poetry", CAT_POETRY,
         "EAL/D", "Texts and human experiences",
         selections="'Journey, the North Coast', 'The Meatworks', 'To the Master, Dōgen Zenji', 'Late Ferry', 'Flames and Dangling Wire', 'Byron Bay: Winter', 'Philip Hodgins (1959-1995)'"),
    Text("Noonuccal, Oodgeroo", "My People", "Poetry", CAT_POETRY,
         "EAL/D", "Texts and human experiences",
         selections="'Corroboree', 'Ballad of the Totems', 'No More Boomerang', 'Son of Mine', 'We Are Going', 'The Past', 'Reed Flute Cave'"),
    Text("Darling, Ian", "Stories of Me", "Media", "Media",
         "EAL/D", "Texts and human experiences"),
    Text("Winton, Tim", "The Boy Behind the Curtain", "Nonfiction", CAT_NONFICTION,
         "EAL/D", "Texts and human experiences",
         selections="'Havoc: A Life in Accidents', 'A Walk at Low Tide', 'Betsy', 'The Wait and the Flow', 'Chasing Giants', 'The Demon Shark'"),
]

# --- EAL/D Focus Area 2: Language, identity and culture ---
EALD_FA2 = [
    Text("Lahiri, Jhumpa", "The Namesake", "Prose fiction", CAT_PROSE,
         "EAL/D", "Language, identity and culture"),
    Text("Winch, Tara June", "Swallow the Air", "Prose fiction", CAT_PROSE,
         "EAL/D", "Language, identity and culture"),
    Text("Antrobus, Raymond", "The Perseverance", "Poetry", CAT_POETRY,
         "EAL/D", "Language, identity and culture",
         selections="'Echo', 'Jamaican British', 'Ode to My Hair', 'Dear Hearing World', 'The Ghost of Laura Bridgman Warns Helen Keller About Fame', 'Dr Marigold Reevaluated', 'To Sweeten Bitter'"),
    Text("Hughes, Langston", "The Collected Poems", "Poetry", CAT_POETRY,
         "EAL/D", "Language, identity and culture",
         selections="'The Negro Speaks of Rivers', 'Mother to Son', 'I, Too', 'The Weary Blues', 'Madam and the Phone Bill', 'Lincoln Theatre', 'Theme for English B'"),
    Text("Law, Michelle", "Miss Peony", "Drama", CAT_DRAMA,
         "EAL/D", "Language, identity and culture"),
    Text("Pung, Alice", "Unpolished Gem", "Nonfiction", CAT_NONFICTION,
         "EAL/D", "Language, identity and culture"),
]

# --- EAL/D Focus Area 3: Close study of text ---
EALD_FA3 = [
    Text("Keegan, Claire", "Small Things Like These", "Prose fiction", CAT_PROSE,
         "EAL/D", "Close study of text"),
    Text("Bradbury, Ray", "Fahrenheit 451", "Prose fiction", CAT_PROSE,
         "EAL/D", "Close study of text"),
    Text("Frost, Robert", "The Collected Poems", "Poetry", CAT_POETRY,
         "EAL/D", "Close study of text",
         selections="'The Tuft of Flowers', 'Mending Wall', 'After Apple-Picking', 'The Road Not Taken', 'Nothing Gold Can Stay', 'Stopping by Woods on a Snowy Evening', 'Acquainted with the Night'"),
    Text("Wright, Judith", "Judith Wright: Collected Poems", "Poetry", CAT_POETRY,
         "EAL/D", "Close study of text",
         selections="'Northern River', 'The Hawthorn Hedge', 'The Bushfire', 'The Killer', 'Flame Tree in a Quarry', 'Train Journey', 'Magpies'"),
    Text("Harrison, Jane", "Rainbow's End", "Drama", CAT_DRAMA,
         "EAL/D", "Close study of text"),
    Text("Villeneuve, Denis", "Arrival", "Film", CAT_FILM,
         "EAL/D", "Close study of text"),
]


# =============================================================================
# EAL/D CONSTRAINT ENGINE
# =============================================================================
# EAL/D: 3 texts, one per focus area.
# Must have one prose fiction, one poetry, one from {drama, film, media, nonfiction}.
# No Shakespeare requirement.

def is_valid_eald_combination(fa1: Text, fa2: Text, fa3: Text) -> bool:
    cats = {
        broad_category(fa1.text_type_category),
        broad_category(fa2.text_type_category),
        broad_category(fa3.text_type_category),
    }
    return CAT_PROSE in cats and CAT_POETRY in cats and bool(cats & OTHER_CATEGORIES)


def generate_all_valid_eald_combinations() -> list[tuple[Text, Text, Text]]:
    valid = []
    for fa1, fa2, fa3 in product(EALD_FA1, EALD_FA2, EALD_FA3):
        if is_valid_eald_combination(fa1, fa2, fa3):
            valid.append((fa1, fa2, fa3))
    return valid


def get_eald_compatible_texts(
    chosen_fa1: Optional[Text] = None,
    chosen_fa2: Optional[Text] = None,
    chosen_fa3: Optional[Text] = None,
) -> tuple[list[Text], list[Text], list[Text]]:
    valid_fa1, valid_fa2, valid_fa3 = [], [], []
    for fa1, fa2, fa3 in product(EALD_FA1, EALD_FA2, EALD_FA3):
        if chosen_fa1 and fa1 != chosen_fa1:
            continue
        if chosen_fa2 and fa2 != chosen_fa2:
            continue
        if chosen_fa3 and fa3 != chosen_fa3:
            continue
        if is_valid_eald_combination(fa1, fa2, fa3):
            if fa1 not in valid_fa1:
                valid_fa1.append(fa1)
            if fa2 not in valid_fa2:
                valid_fa2.append(fa2)
            if fa3 not in valid_fa3:
                valid_fa3.append(fa3)
    return valid_fa1, valid_fa2, valid_fa3


def count_remaining_eald(
    chosen_fa1: Optional[Text] = None,
    chosen_fa2: Optional[Text] = None,
    chosen_fa3: Optional[Text] = None,
) -> int:
    count = 0
    for fa1, fa2, fa3 in product(EALD_FA1, EALD_FA2, EALD_FA3):
        if chosen_fa1 and fa1 != chosen_fa1:
            continue
        if chosen_fa2 and fa2 != chosen_fa2:
            continue
        if chosen_fa3 and fa3 != chosen_fa3:
            continue
        if is_valid_eald_combination(fa1, fa2, fa3):
            count += 1
    return count


# =============================================================================
# EXTENSION 1 TEXTS
# =============================================================================

EXT1_ELECTIVE_FULL_NAMES = [
    "Elective 1: Confessional worlds",
    "Elective 2: Historical worlds",
    "Elective 3: Hybrid worlds",
    "Elective 4: Natural worlds",
    "Elective 5: Shakespearean worlds",
]

EXT1_ELECTIVE_NAMES = [
    "Confessional worlds",
    "Historical worlds",
    "Hybrid worlds",
    "Natural worlds",
    "Shakespearean worlds",
]

EXT1_TEXTS: list[list[Text]] = [

    # Elective 1: Confessional worlds
    [
        Text("Brontë, Anne", "The Tenant of Wildfell Hall", "Prose fiction", CAT_PROSE,
             "Extension 1", "Confessional worlds"),
        Text("Didion, Joan", "The White Album", "Nonfiction", CAT_NONFICTION,
             "Extension 1", "Confessional worlds",
             selections="'The White Album', 'Holy Water', 'Bureaucrats', 'Good Citizens', 'Notes Toward a Dreampolitik'"),
        Text("Hughes, Ted", "Birthday Letters", "Poetry", CAT_POETRY,
             "Extension 1", "Confessional worlds",
             selections="'The Shot', 'Trophies', 'Moonwalk', 'Error', 'A Short Film', 'The Beach', 'A Picture of Otto'"),
        Text("Mansfield, Katherine", "The Collected Stories", "Prose fiction", CAT_PROSE,
             "Extension 1", "Confessional worlds",
             selections="'Prelude', 'Je ne Parle pas Francais', 'Bliss', 'Psychology', 'The Daughters of the Late Colonel'"),
        Text("Williams, Tennessee", "The Glass Menagerie", "Drama", CAT_DRAMA,
             "Extension 1", "Confessional worlds"),
        Text("Anderson, Wes", "The Darjeeling Limited", "Film", CAT_FILM,
             "Extension 1", "Confessional worlds"),
    ],

    # Elective 2: Historical worlds
    [
        Text("Auden, WH", "Selected Poems", "Poetry", CAT_POETRY,
             "Extension 1", "Historical worlds",
             selections="'Spain', 'In Memory of W.B. Yeats', 'September 1, 1939', 'Memorial for the City', 'The Shield of Achilles', 'Moon Landing', 'Archaeology'"),
        Text("Byatt, AS", "Possession", "Prose fiction", CAT_PROSE,
             "Extension 1", "Historical worlds"),
        Text("de Waal, Edmund", "The Hare with Amber Eyes", "Nonfiction", CAT_NONFICTION,
             "Extension 1", "Historical worlds"),
        Text("Gaskell, Elizabeth", "North and South", "Prose fiction", CAT_PROSE,
             "Extension 1", "Historical worlds"),
        Text("Ishiguro, Kazuo", "An Artist of the Floating World", "Prose fiction", CAT_PROSE,
             "Extension 1", "Historical worlds"),
        Text("Coppola, Sofia", "Marie Antoinette", "Film", CAT_FILM,
             "Extension 1", "Historical worlds"),
    ],

    # Elective 3: Hybrid worlds
    [
        Text("Araluen, Evelyn", "Dropbear", "Poetry", CAT_POETRY,
             "Extension 1", "Hybrid worlds",
             selections="'Index Australis', 'Playing in the Pastoral', 'The Trope Speaks', 'Bad Taxidermy', 'Mrs Kookaburra Addresses the Natives', 'To the Parents', 'THE LAST BUSH BALLAD'"),
        Text("Austen, Jane", "Northanger Abbey", "Prose fiction", CAT_PROSE,
             "Extension 1", "Hybrid worlds"),
        Text("Faulkner, William", "As I Lay Dying", "Prose fiction", CAT_PROSE,
             "Extension 1", "Hybrid worlds"),
        Text("Smith, Tracy K", "Life on Mars", "Poetry", CAT_POETRY,
             "Extension 1", "Hybrid worlds",
             selections="'Sci-Fi', 'My God, It\u2019s Full of Stars', 'The Museum of Obsolescence', 'The Universe: Original Motion Picture Soundtrack', 'They May Love All That He Has Chosen and Hate All That He Has Rejected', 'The Universe as Primal Scream', 'Everything That Ever Was'"),
        Text("Wallace, David Foster", "Consider the Lobster", "Nonfiction", CAT_NONFICTION,
             "Extension 1", "Hybrid worlds",
             selections="'Authority and American Usage', 'The View from Mrs Thompson\u2019s', 'How Tracy Austin Broke My Heart', 'Up, Simba', 'Consider the Lobster'"),
        Text("Nolan, Christopher", "Memento", "Film", CAT_FILM,
             "Extension 1", "Hybrid worlds"),
    ],

    # Elective 4: Natural worlds
    [
        Text("Coleridge, Samuel Taylor", "Samuel Taylor Coleridge: The Complete Poems", "Poetry", CAT_POETRY,
             "Extension 1", "Natural worlds",
             selections="'The Eolian Harp', 'This Lime-Tree Bower My Prison', 'The Rime of the Ancient Mariner' (1834), 'Frost at Midnight'"),
        Text("MacLeod, Alistair", "Island", "Prose fiction", CAT_PROSE,
             "Extension 1", "Natural worlds",
             selections="'The Boat', 'In the Fall', 'The Lost Salt Gift of Blood', 'The Road to Rankin\u2019s Point', 'Winter Dog', 'The Tuning of Perfection', 'Clearances'"),
        Text("Oliver, Mary", "New and Selected Poems, Volume One", "Poetry", CAT_POETRY,
             "Extension 1", "Natural worlds",
             selections="'When Death Comes', 'The Waterfall', 'The Sun', 'The Swan', 'Morning Poem', 'Wild Geese', 'Sleeping in the Forest', 'Aunt Leaf'"),
        Text("Shakespeare, William", "As You Like It", "Drama, Shakespearean text", CAT_SHAKESPEARE,
             "Extension 1", "Natural worlds", is_shakespeare=True),
        Text("Smith, Ali", "Autumn", "Prose fiction", CAT_PROSE,
             "Extension 1", "Natural worlds"),
        Text("Yunkaporta, Tyson", "Sand Talk", "Nonfiction", CAT_NONFICTION,
             "Extension 1", "Natural worlds"),
    ],

    # Elective 5: Shakespearean worlds
    [
        Text("Al Bassam, Sulayman", "The Arab Shakespeare Trilogy", "Drama", CAT_DRAMA,
             "Extension 1", "Shakespearean worlds"),
        Text("Atwood, Margaret", "Hag-Seed", "Prose fiction", CAT_PROSE,
             "Extension 1", "Shakespearean worlds"),
        Text("Shakespeare, William", "The Merchant of Venice", "Drama, Shakespearean text", CAT_SHAKESPEARE,
             "Extension 1", "Shakespearean worlds", is_shakespeare=True),
        Text("Shapiro, James", "1599: A Year in the Life of William Shakespeare", "Nonfiction", CAT_NONFICTION,
             "Extension 1", "Shakespearean worlds"),
        Text("Stoppard, Tom", "Rosencrantz and Guildenstern are Dead", "Drama", CAT_DRAMA,
             "Extension 1", "Shakespearean worlds"),
        Text("McKay, Adam", "The Big Short", "Film", CAT_FILM,
             "Extension 1", "Shakespearean worlds"),
    ],
]


# =============================================================================
# EXTENSION 1 CONSTRAINT ENGINE
# =============================================================================
# Pick 3 texts from ONE elective.
# At least 2 must be extended print texts (prose fiction, nonfiction, poetry, or drama).
# Only Film and Media/multimodal texts are NOT extended print texts.

def is_print_ext1(text: Text) -> bool:
    """Extended print text: excludes only film and media (not drama)."""
    return broad_category(text.text_type_category) not in {CAT_FILM, "Media"}


def is_valid_ext1_combo(texts: list[Text]) -> bool:
    """3 texts, at least 2 extended print."""
    return sum(1 for t in texts if is_print_ext1(t)) >= 2


def get_ext1_available(elective_idx: int, chosen_idxs: list[int]) -> list[int]:
    """Return indices still available in the elective given current chosen_idxs."""
    texts = EXT1_TEXTS[elective_idx]
    chosen_texts = [texts[i] for i in chosen_idxs]
    available = []
    for i, t in enumerate(texts):
        if i in chosen_idxs:
            continue
        potential = chosen_texts + [t]
        if len(potential) == 3:
            if is_valid_ext1_combo(potential):
                available.append(i)
        else:
            remaining = [x for j, x in enumerate(texts) if j not in chosen_idxs and j != i]
            if any(is_valid_ext1_combo(potential + [r]) for r in remaining):
                available.append(i)
    return available


def generate_all_valid_ext1_combos() -> list[tuple[int, int, int, int]]:
    """Returns (elective_idx, t1_idx, t2_idx, t3_idx) for every valid trio."""
    valid = []
    for e_idx, elective_texts in enumerate(EXT1_TEXTS):
        for i, j, k in combinations(range(len(elective_texts)), 3):
            if is_valid_ext1_combo([elective_texts[i], elective_texts[j], elective_texts[k]]):
                valid.append((e_idx, i, j, k))
    return valid


# Quick stats on load
if __name__ == "__main__":
    total = len(ADVANCED_TC_PAIRS) * len(ADVANCED_CRIT) * len(ADVANCED_COMMON)
    valid = generate_all_valid_combinations()
    print(f"Advanced: {total} total combinations, {len(valid)} valid")
    print(f"  TC pairs: {len(ADVANCED_TC_PAIRS)}")
    print(f"  Critical study texts: {len(ADVANCED_CRIT)}")
    print(f"  Common module texts: {len(ADVANCED_COMMON)}")

    total_s = len(STANDARD_COMMON) * len(STANDARD_LIC) * len(STANDARD_CLOSE)
    valid_s = generate_all_valid_standard_combinations()
    print(f"\nStandard: {total_s} total combinations, {len(valid_s)} valid")
    print(f"  Common texts: {len(STANDARD_COMMON)}")
    print(f"  LIC texts: {len(STANDARD_LIC)}")
    print(f"  Close study texts: {len(STANDARD_CLOSE)}")

    total_e = len(EALD_FA1) * len(EALD_FA2) * len(EALD_FA3)
    valid_e = generate_all_valid_eald_combinations()
    print(f"\nEAL/D: {total_e} total combinations, {len(valid_e)} valid")
    print(f"  FA1 texts: {len(EALD_FA1)}")
    print(f"  FA2 texts: {len(EALD_FA2)}")
    print(f"  FA3 texts: {len(EALD_FA3)}")

    valid_x = generate_all_valid_ext1_combos()
    print(f"\nExtension 1: {len(valid_x)} valid combinations across {len(EXT1_TEXTS)} electives")
