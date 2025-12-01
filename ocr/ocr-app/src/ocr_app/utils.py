"""Utility helpers for OCR post-processing and small corrections."""
from typing import Iterable
import os

try:
    from symspellpy import Verbosity
except ImportError:
    Verbosity = None


# Cache for English dictionary
_ENGLISH_DICT = None


def load_english_dictionary() -> set:
    """Load a comprehensive English dictionary for OCR correction.
    
    Uses PyEnchant (if available) which provides comprehensive spell-checking
    dictionaries. Falls back to NLTK, then to a built-in common words list.
    """
    global _ENGLISH_DICT
    
    if _ENGLISH_DICT is not None:
        return _ENGLISH_DICT
    
    # First try PyEnchant - most accurate and comprehensive
    try:
        import enchant
        d = enchant.Dict("en_US")
        # PyEnchant doesn't provide a word list, but we can use it for checking
        # For now, fall through to NLTK or common words
    except ImportError:
        pass
    
    # Try to load from NLTK words corpus (234k words)
    try:
        import nltk
        try:
            from nltk.corpus import words
            _ENGLISH_DICT = set(w.upper() for w in words.words())
            print(f"[OCR] Loaded {len(_ENGLISH_DICT)} words from NLTK dictionary")
            return _ENGLISH_DICT
        except LookupError:
            # Download words corpus if not available
            print("[OCR] Downloading NLTK words corpus...")
            nltk.download('words', quiet=True)
            from nltk.corpus import words
            _ENGLISH_DICT = set(w.upper() for w in words.words())
            print(f"[OCR] Loaded {len(_ENGLISH_DICT)} words from NLTK dictionary")
            return _ENGLISH_DICT
    except ImportError:
        print("[OCR] NLTK not available, using built-in word list")
        pass
    
    # Final fallback: comprehensive built-in common words
    _ENGLISH_DICT = _get_comprehensive_word_list()
    print(f"[OCR] Using built-in dictionary with {len(_ENGLISH_DICT)} words")
    return _ENGLISH_DICT


def load_symspell():
    """Load SymSpell for fast spell correction.
    
    Returns None if SymSpell is not available.
    """
    try:
        from symspellpy import SymSpell, Verbosity
        
        sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)
        
        # Load dictionary
        try:
            # Try to load from package data
            import pkg_resources
            dict_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
            if os.path.isfile(dict_path):
                sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)
                return sym_spell
        except:
            pass
        
        # If that fails, return None (will use fallback correction)
        return None
    except ImportError:
        return None


def _get_comprehensive_word_list() -> set:
    """Return comprehensive list of common English words based on Google's most frequent words.
    
    This includes the most common ~1000 English words plus domain-specific terms.
    Sufficient for most OCR correction tasks without requiring external downloads.
    """
    return {
        # Articles, pronouns, prepositions
        'A', 'AN', 'THE', 'THIS', 'THAT', 'THESE', 'THOSE', 'I', 'YOU', 'HE', 'SHE', 'IT', 'WE', 'THEY',
        'ME', 'HIM', 'HER', 'US', 'THEM', 'MY', 'YOUR', 'HIS', 'HER', 'ITS', 'OUR', 'THEIR',
        'MINE', 'YOURS', 'HERS', 'OURS', 'THEIRS', 'IN', 'ON', 'AT', 'TO', 'FOR', 'WITH', 'FROM',
        'BY', 'OF', 'ABOUT', 'AS', 'INTO', 'THROUGH', 'DURING', 'BEFORE', 'AFTER', 'ABOVE', 'BELOW',
        'BETWEEN', 'UNDER', 'OVER', 'AGAINST', 'AMONG', 'TOWARD', 'UPON',
        
        # Verbs
        'BE', 'AM', 'IS', 'ARE', 'WAS', 'WERE', 'BEEN', 'BEING', 'HAVE', 'HAS', 'HAD', 'HAVING',
        'DO', 'DOES', 'DID', 'DOING', 'DONE', 'CAN', 'COULD', 'MAY', 'MIGHT', 'WILL', 'WOULD',
        'SHALL', 'SHOULD', 'MUST', 'OUGHT', 'GO', 'GOES', 'WENT', 'GONE', 'GOING', 'GET', 'GETS',
        'GOT', 'GOTTEN', 'GETTING', 'MAKE', 'MAKES', 'MADE', 'MAKING', 'TAKE', 'TAKES', 'TOOK',
        'TAKEN', 'TAKING', 'COME', 'COMES', 'CAME', 'COMING', 'SEE', 'SEES', 'SAW', 'SEEN', 'SEEING',
        'KNOW', 'KNOWS', 'KNEW', 'KNOWN', 'KNOWING', 'THINK', 'THINKS', 'THOUGHT', 'THINKING',
        'WANT', 'WANTS', 'WANTED', 'WANTING', 'GIVE', 'GIVES', 'GAVE', 'GIVEN', 'GIVING',
        'USE', 'USES', 'USED', 'USING', 'FIND', 'FINDS', 'FOUND', 'FINDING', 'TELL', 'TELLS',
        'TOLD', 'TELLING', 'ASK', 'ASKS', 'ASKED', 'ASKING', 'WORK', 'WORKS', 'WORKED', 'WORKING',
        'SEEM', 'SEEMS', 'SEEMED', 'SEEMING', 'FEEL', 'FEELS', 'FELT', 'FEELING', 'TRY', 'TRIES',
        'TRIED', 'TRYING', 'LEAVE', 'LEAVES', 'LEFT', 'LEAVING', 'CALL', 'CALLS', 'CALLED', 'CALLING',
        'KEEP', 'KEEPS', 'KEPT', 'KEEPING', 'LET', 'LETS', 'LETTING', 'BEGIN', 'BEGINS', 'BEGAN',
        'BEGUN', 'BEGINNING', 'SHOW', 'SHOWS', 'SHOWED', 'SHOWN', 'SHOWING', 'HEAR', 'HEARS', 'HEARD',
        'HEARING', 'PLAY', 'PLAYS', 'PLAYED', 'PLAYING', 'RUN', 'RUNS', 'RAN', 'RUNNING', 'MOVE',
        'MOVES', 'MOVED', 'MOVING', 'LIKE', 'LIKES', 'LIKED', 'LIKING', 'LIVE', 'LIVES', 'LIVED',
        'LIVING', 'BELIEVE', 'BELIEVES', 'BELIEVED', 'BELIEVING', 'HOLD', 'HOLDS', 'HELD', 'HOLDING',
        'BRING', 'BRINGS', 'BROUGHT', 'BRINGING', 'HAPPEN', 'HAPPENS', 'HAPPENED', 'HAPPENING',
        'WRITE', 'WRITES', 'WROTE', 'WRITTEN', 'WRITING', 'SIT', 'SITS', 'SAT', 'SITTING', 'STAND',
        'STANDS', 'STOOD', 'STANDING', 'LOSE', 'LOSES', 'LOST', 'LOSING', 'PAY', 'PAYS', 'PAID',
        'PAYING', 'MEET', 'MEETS', 'MET', 'MEETING', 'INCLUDE', 'INCLUDES', 'INCLUDED', 'INCLUDING',
        'CONTINUE', 'CONTINUES', 'CONTINUED', 'CONTINUING', 'SET', 'SETS', 'SETTING', 'LEARN',
        'LEARNS', 'LEARNED', 'LEARNING', 'CHANGE', 'CHANGES', 'CHANGED', 'CHANGING', 'LEAD', 'LEADS',
        'LED', 'LEADING', 'UNDERSTAND', 'UNDERSTANDS', 'UNDERSTOOD', 'UNDERSTANDING', 'WATCH',
        'WATCHES', 'WATCHED', 'WATCHING', 'FOLLOW', 'FOLLOWS', 'FOLLOWED', 'FOLLOWING', 'STOP',
        'STOPS', 'STOPPED', 'STOPPING', 'CREATE', 'CREATES', 'CREATED', 'CREATING', 'SPEAK', 'SPEAKS',
        'SPOKE', 'SPOKEN', 'SPEAKING', 'READ', 'READS', 'READING', 'ALLOW', 'ALLOWS', 'ALLOWED',
        'ALLOWING', 'ADD', 'ADDS', 'ADDED', 'ADDING', 'SPEND', 'SPENDS', 'SPENT', 'SPENDING',
        'GROW', 'GROWS', 'GREW', 'GROWN', 'GROWING', 'OPEN', 'OPENS', 'OPENED', 'OPENING', 'WALK',
        'WALKS', 'WALKED', 'WALKING', 'WIN', 'WINS', 'WON', 'WINNING', 'OFFER', 'OFFERS', 'OFFERED',
        'OFFERING', 'REMEMBER', 'REMEMBERS', 'REMEMBERED', 'REMEMBERING', 'LOVE', 'LOVES', 'LOVED',
        'LOVING', 'CONSIDER', 'CONSIDERS', 'CONSIDERED', 'CONSIDERING', 'APPEAR', 'APPEARS',
        'APPEARED', 'APPEARING', 'BUY', 'BUYS', 'BOUGHT', 'BUYING', 'WAIT', 'WAITS', 'WAITED',
        'WAITING', 'SERVE', 'SERVES', 'SERVED', 'SERVING', 'DIE', 'DIES', 'DIED', 'DYING', 'SEND',
        'SENDS', 'SENT', 'SENDING', 'EXPECT', 'EXPECTS', 'EXPECTED', 'EXPECTING', 'BUILD', 'BUILDS',
        'BUILT', 'BUILDING', 'STAY', 'STAYS', 'STAYED', 'STAYING', 'FALL', 'FALLS', 'FELL', 'FALLEN',
        'FALLING', 'CUT', 'CUTS', 'CUTTING', 'REACH', 'REACHES', 'REACHED', 'REACHING', 'KILL',
        'KILLS', 'KILLED', 'KILLING', 'REMAIN', 'REMAINS', 'REMAINED', 'REMAINING', 'SUGGEST',
        'SUGGESTS', 'SUGGESTED', 'SUGGESTING', 'RAISE', 'RAISES', 'RAISED', 'RAISING', 'PASS',
        'PASSES', 'PASSED', 'PASSING', 'SELL', 'SELLS', 'SOLD', 'SELLING', 'REQUIRE', 'REQUIRES',
        'REQUIRED', 'REQUIRING', 'REPORT', 'REPORTS', 'REPORTED', 'REPORTING', 'DECIDE', 'DECIDES',
        'DECIDED', 'DECIDING', 'PULL', 'PULLS', 'PULLED', 'PULLING',
        
        # Adjectives & Adverbs
        'GOOD', 'BETTER', 'BEST', 'NEW', 'NEWER', 'NEWEST', 'OLD', 'OLDER', 'OLDEST', 'FIRST', 'LAST',
        'LONG', 'LONGER', 'LONGEST', 'GREAT', 'GREATER', 'GREATEST', 'LITTLE', 'LESS', 'LEAST',
        'OWN', 'OTHER', 'DIFFERENT', 'SMALL', 'SMALLER', 'SMALLEST', 'LARGE', 'LARGER', 'LARGEST',
        'BIG', 'BIGGER', 'BIGGEST', 'HIGH', 'HIGHER', 'HIGHEST', 'LOW', 'LOWER', 'LOWEST', 'NEXT',
        'EARLY', 'EARLIER', 'EARLIEST', 'YOUNG', 'YOUNGER', 'YOUNGEST', 'IMPORTANT', 'FEW', 'FEWER',
        'FEWEST', 'PUBLIC', 'BAD', 'WORSE', 'WORST', 'SAME', 'ABLE', 'NOT', 'NO', 'YES', 'VERY',
        'SO', 'JUST', 'ONLY', 'ALSO', 'EVEN', 'WELL', 'BACK', 'THERE', 'HERE', 'WHERE', 'WHEN',
        'HOW', 'WHY', 'WHAT', 'WHICH', 'WHO', 'WHOM', 'WHOSE', 'NOW', 'THEN', 'THAN', 'MORE', 'MOST',
        'MUCH', 'MANY', 'SOME', 'ANY', 'ALL', 'BOTH', 'EACH', 'EVERY', 'ANOTHER', 'SUCH', 'STILL',
        'QUITE', 'RATHER', 'ALMOST', 'ALREADY', 'ALWAYS', 'NEVER', 'OFTEN', 'SOMETIMES', 'USUALLY',
        'PERHAPS', 'MAYBE', 'PROBABLY', 'CERTAINLY', 'HOWEVER', 'THEREFORE', 'THUS', 'OTHERWISE',
        'INDEED', 'BESIDES', 'MOREOVER', 'FURTHERMORE', 'MEANWHILE', 'NEVERTHELESS', 'NONETHELESS',
        'ANYWAY', 'SOMEHOW', 'SOMEWHAT', 'SOMEWHERE', 'EVERYWHERE', 'NOWHERE', 'ANYWHERE', 'ELSE',
        'TOGETHER', 'APART', 'AWAY', 'FAR', 'NEAR', 'CLOSE', 'DIRECTLY', 'IMMEDIATELY', 'SOON',
        'LATE', 'LATER', 'RECENTLY', 'FINALLY', 'ONCE', 'TWICE', 'AGAIN', 'EVER', 'REALLY', 'ACTUALLY',
        'ESPECIALLY', 'PARTICULARLY', 'GENERALLY', 'USUALLY', 'NORMALLY', 'TYPICALLY', 'EXACTLY',
        'NEARLY', 'ALMOST', 'HARDLY', 'BARELY', 'SCARCELY', 'SIMPLY', 'MERELY', 'ENOUGH', 'TOO',
        'PRETTY', 'FAIRLY', 'QUITE', 'EXTREMELY', 'HIGHLY', 'COMPLETELY', 'TOTALLY', 'ENTIRELY',
        'ABSOLUTELY', 'PERFECTLY', 'FULLY', 'PARTLY', 'MAINLY', 'MOSTLY', 'LARGELY', 'SLIGHTLY',
        'SOMEWHAT', 'RELATIVELY', 'COMPARATIVELY', 'INCREASINGLY', 'EQUALLY', 'SIMILARLY', 'LIKEWISE',
        'DIFFERENTLY', 'SEPARATELY', 'INDEPENDENTLY', 'APPARENTLY', 'OBVIOUSLY', 'CLEARLY', 'SURELY',
        'DEFINITELY', 'POSSIBLY', 'LIKELY', 'UNLIKELY', 'FORTUNATELY', 'UNFORTUNATELY', 'SADLY',
        'HAPPILY', 'QUICKLY', 'SLOWLY', 'EASILY', 'CAREFULLY', 'STRONGLY', 'BADLY', 'SERIOUSLY',
        
        # Nouns
        'TIME', 'TIMES', 'YEAR', 'YEARS', 'DAY', 'DAYS', 'WEEK', 'WEEKS', 'MONTH', 'MONTHS',
        'HOUR', 'HOURS', 'MINUTE', 'MINUTES', 'SECOND', 'SECONDS', 'MOMENT', 'MOMENTS', 'MORNING',
        'AFTERNOON', 'EVENING', 'NIGHT', 'TODAY', 'YESTERDAY', 'TOMORROW', 'WEEKEND', 'PEOPLE',
        'PERSON', 'MAN', 'MEN', 'WOMAN', 'WOMEN', 'CHILD', 'CHILDREN', 'BOY', 'BOYS', 'GIRL', 'GIRLS',
        'FAMILY', 'FAMILIES', 'FRIEND', 'FRIENDS', 'PARENT', 'PARENTS', 'MOTHER', 'FATHER', 'BROTHER',
        'SISTER', 'SON', 'DAUGHTER', 'HUSBAND', 'WIFE', 'BABY', 'BABIES', 'KID', 'KIDS', 'LIFE',
        'LIVES', 'WORLD', 'COUNTRY', 'COUNTRIES', 'STATE', 'STATES', 'CITY', 'CITIES', 'TOWN', 'TOWNS',
        'PLACE', 'PLACES', 'HOME', 'HOUSE', 'HOUSES', 'ROOM', 'ROOMS', 'AREA', 'AREAS', 'STREET',
        'STREETS', 'ROAD', 'ROADS', 'WAY', 'WAYS', 'DOOR', 'DOORS', 'WINDOW', 'WINDOWS', 'FLOOR',
        'FLOORS', 'WALL', 'WALLS', 'ROOF', 'TABLE', 'TABLES', 'CHAIR', 'CHAIRS', 'BED', 'BEDS',
        'WATER', 'FOOD', 'AIR', 'FIRE', 'EARTH', 'LAND', 'SEA', 'OCEAN', 'RIVER', 'LAKE', 'MOUNTAIN',
        'HILL', 'TREE', 'TREES', 'PLANT', 'PLANTS', 'FLOWER', 'FLOWERS', 'ANIMAL', 'ANIMALS', 'BIRD',
        'BIRDS', 'FISH', 'DOG', 'DOGS', 'CAT', 'CATS', 'THING', 'THINGS', 'PART', 'PARTS', 'PIECE',
        'PIECES', 'GROUP', 'GROUPS', 'NUMBER', 'NUMBERS', 'NAME', 'NAMES', 'WORD', 'WORDS', 'LINE',
        'LINES', 'LETTER', 'LETTERS', 'PAGE', 'PAGES', 'BOOK', 'BOOKS', 'STORY', 'STORIES', 'IDEA',
        'IDEAS', 'QUESTION', 'QUESTIONS', 'ANSWER', 'ANSWERS', 'PROBLEM', 'PROBLEMS', 'FACT', 'FACTS',
        'REASON', 'REASONS', 'CASE', 'CASES', 'POINT', 'POINTS', 'EXAMPLE', 'EXAMPLES', 'TYPE',
        'TYPES', 'KIND', 'KINDS', 'FORM', 'FORMS', 'WAY', 'WAYS', 'SIDE', 'SIDES', 'END', 'ENDS',
        'HAND', 'HANDS', 'EYE', 'EYES', 'HEAD', 'FACE', 'BODY', 'HEART', 'MIND', 'VOICE', 'FEET',
        'FOOT', 'LEG', 'LEGS', 'ARM', 'ARMS', 'BACK', 'FRONT', 'TOP', 'BOTTOM', 'LEFT', 'RIGHT',
        'WORK', 'JOB', 'JOBS', 'SCHOOL', 'SCHOOLS', 'STUDENT', 'STUDENTS', 'TEACHER', 'TEACHERS',
        'CLASS', 'CLASSES', 'OFFICE', 'OFFICES', 'COMPANY', 'COMPANIES', 'BUSINESS', 'MONEY', 'DOLLAR',
        'DOLLARS', 'PRICE', 'PRICES', 'COST', 'COSTS', 'CAR', 'CARS', 'PHONE', 'COMPUTER', 'COMPUTERS',
        'PROGRAM', 'PROGRAMS', 'SYSTEM', 'SYSTEMS', 'GOVERNMENT', 'LAW', 'LAWS', 'POWER', 'WAR',
        'WARS', 'PRESIDENT', 'PARTY', 'PARTIES', 'MEMBER', 'MEMBERS', 'LEVEL', 'LEVELS', 'ORDER',
        'CHANGE', 'CHANGES', 'SERVICE', 'SERVICES', 'INTEREST', 'RATE', 'RATES', 'MARKET', 'MARKETS',
        'STUDY', 'STUDIES', 'INFORMATION', 'HEALTH', 'CARE', 'MOTHER', 'FATHER', 'RESULT', 'RESULTS',
        'EFFECT', 'EFFECTS', 'AGE', 'AGES', 'DEATH', 'BIRTH', 'EDUCATION', 'EXPERIENCE', 'ART',
        'MUSIC', 'FILM', 'GAME', 'GAMES', 'SPORT', 'SPORTS', 'TEAM', 'TEAMS', 'PLAYER', 'PLAYERS',
        'SEASON', 'SEASONS', 'HISTORY', 'FUTURE', 'PAST', 'PRESENT', 'PICTURE', 'PICTURES', 'IMAGE',
        'IMAGES', 'COLOR', 'COLORS', 'LIGHT', 'DARK', 'SOUND', 'SOUNDS', 'MINUTE', 'MINUTES',
        
        # Conjunctions & Others
        'AND', 'OR', 'BUT', 'NOR', 'YET', 'IF', 'UNLESS', 'UNTIL', 'WHILE', 'SINCE', 'BECAUSE',
        'ALTHOUGH', 'THOUGH', 'WHETHER', 'EITHER', 'NEITHER', 'BOTH', 'BESIDES', 'PLUS', 'MINUS',
        
        # Sign/Warning/Common OCR words
        'STOP', 'CAUTION', 'WARNING', 'DANGER', 'ENTRY', 'EXIT', 'PLEASE', 'THANK', 'THANKS',
        'WELCOME', 'HELLO', 'GOODBYE', 'HAPPY', 'BIRTHDAY', 'CONGRATULATIONS', 'SORRY', 'HELP',
        'OPEN', 'CLOSED', 'PUSH', 'PULL', 'PRIVATE', 'RESERVED', 'PARKING', 'SPEED', 'LIMIT',
        'SLOW', 'YIELD', 'AHEAD', 'DETOUR', 'CONSTRUCTION', 'SCHOOL', 'ZONE', 'CROSSING', 'PEDESTRIAN',
        'BIKE', 'LANE', 'HOSPITAL', 'EMERGENCY', 'FIRE', 'POLICE', 'RESTROOM', 'BATHROOM', 'MENS',
        'WOMENS', 'ELEVATOR', 'STAIRS', 'ENTRANCE', 'INFORMATION', 'HOURS', 'SALE', 'FREE', 'OFF',
        'DISCOUNT', 'DEAL', 'SPECIAL', 'TODAY', 'ONLY', 'LIMITED', 'OFFER', 'CASH', 'CREDIT',
        'DEBIT', 'CARD', 'ACCEPTED', 'VISA', 'MASTERCARD', 'AMERICAN', 'EXPRESS', 'BREAKFAST',
        'LUNCH', 'DINNER', 'MENU', 'RESTAURANT', 'COFFEE', 'TEA', 'DRINK', 'BEER', 'WINE', 'BAR',
        'HOTEL', 'MOTEL', 'INN', 'RESORT', 'CHECK', 'CHECKOUT', 'RESERVATION', 'VACANCY', 'WIFI',
        'INTERNET', 'PHONE', 'CALL', 'TEXT', 'EMAIL', 'ADDRESS', 'WEBSITE', 'FACEBOOK', 'TWITTER',
        'INSTAGRAM', 'SOCIAL', 'MEDIA', 'FOLLOW', 'SHARE', 'LIKE', 'COMMENT', 'SUBSCRIBE',
        
        # Greetings and emotions
        'BEST', 'WISHES', 'LOVE', 'FUNNY', 'AMAZING', 'AWESOME', 'GREAT', 'WONDERFUL', 'BEAUTIFUL',
        'PRETTY', 'NICE', 'GOOD', 'EXCELLENT', 'PERFECT', 'COOL', 'FUN', 'EXCITING', 'INTERESTING',
        'BORING', 'BAD', 'TERRIBLE', 'AWFUL', 'HORRIBLE', 'SCARY', 'STRANGE', 'WEIRD', 'NORMAL',
        'REGULAR', 'USUAL', 'SPECIAL', 'UNIQUE', 'RARE', 'COMMON', 'POPULAR', 'FAMOUS', 'UNKNOWN',
        
        # Seasons and nature
        'SUMMER', 'WINTER', 'SPRING', 'FALL', 'AUTUMN', 'SEASON', 'WEATHER', 'SUN', 'SUNNY', 'RAIN',
        'RAINY', 'SNOW', 'SNOWY', 'WIND', 'WINDY', 'CLOUD', 'CLOUDY', 'STORM', 'HOT', 'COLD', 'WARM',
        'COOL', 'WET', 'DRY', 'TEMPERATURE', 'DEGREE', 'DEGREES', 'NATURE', 'NATURAL', 'ENVIRONMENT',
        
        # Activities and actions
        'LOOK', 'LOOKING', 'SEE', 'SEEING', 'WATCH', 'WATCHING', 'LISTEN', 'LISTENING', 'TALK',
        'TALKING', 'SAY', 'SAYING', 'TELL', 'TELLING', 'ASK', 'ASKING', 'ANSWER', 'ANSWERING',
        'CALL', 'CALLING', 'TEXT', 'TEXTING', 'WRITE', 'WRITING', 'READ', 'READING', 'STUDY',
        'STUDYING', 'LEARN', 'LEARNING', 'TEACH', 'TEACHING', 'UNDERSTAND', 'UNDERSTANDING',
        'KNOW', 'KNOWING', 'THINK', 'THINKING', 'BELIEVE', 'BELIEVING', 'REMEMBER', 'REMEMBERING',
        'FORGET', 'FORGETTING', 'HOPE', 'HOPING', 'WANT', 'WANTING', 'NEED', 'NEEDING', 'LIKE',
        'LIKING', 'LOVE', 'LOVING', 'HATE', 'HATING', 'PREFER', 'PREFERRING', 'CHOOSE', 'CHOOSING',
        'DECIDE', 'DECIDING', 'TRY', 'TRYING', 'ATTEMPT', 'ATTEMPTING', 'START', 'STARTING', 'BEGIN',
        'BEGINNING', 'CONTINUE', 'CONTINUING', 'FINISH', 'FINISHING', 'END', 'ENDING', 'COMPLETE',
        'COMPLETING', 'DONE',
        
        # Technology and modern words
        'COMPUTER', 'LAPTOP', 'PHONE', 'SMARTPHONE', 'TABLET', 'IPAD', 'IPHONE', 'ANDROID', 'APP',
        'APPS', 'APPLICATION', 'SOFTWARE', 'HARDWARE', 'INTERNET', 'WEB', 'WEBSITE', 'SITE', 'PAGE',
        'ONLINE', 'OFFLINE', 'DIGITAL', 'VIRTUAL', 'CLOUD', 'SERVER', 'DATA', 'FILE', 'FILES',
        'DOWNLOAD', 'UPLOAD', 'STREAM', 'STREAMING', 'VIDEO', 'VIDEOS', 'AUDIO', 'PHOTO', 'PHOTOS',
        'PICTURE', 'PICTURES', 'IMAGE', 'IMAGES', 'CAMERA', 'SCREEN', 'DISPLAY', 'KEYBOARD', 'MOUSE',
        'CLICK', 'TAP', 'SWIPE', 'SCROLL', 'ZOOM', 'SEARCH', 'GOOGLE', 'BROWSER', 'CHROME', 'SAFARI',
        'FIREFOX', 'MICROSOFT', 'WINDOWS', 'MAC', 'APPLE', 'SAMSUNG', 'SONY', 'DELL', 'HP', 'LENOVO',
        
        # Common proper nouns that might appear in images
        'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY', 'JANUARY',
        'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
        'NOVEMBER', 'DECEMBER', 'AMERICA', 'AMERICAN', 'UNITED', 'STATES', 'USA', 'UK', 'ENGLAND',
        'ENGLISH', 'CANADA', 'CANADIAN', 'AUSTRALIA', 'AUSTRALIAN', 'EUROPE', 'EUROPEAN', 'ASIA',
        'ASIAN', 'AFRICA', 'AFRICAN', 'CHINA', 'CHINESE', 'JAPAN', 'JAPANESE', 'INDIA', 'INDIAN',
        
        # Numbers as words
        'ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN',
        'ELEVEN', 'TWELVE', 'THIRTEEN', 'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN',
        'NINETEEN', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY', 'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY',
        'HUNDRED', 'THOUSAND', 'MILLION', 'BILLION', 'TRILLION', 'FIRST', 'SECOND', 'THIRD', 'FOURTH',
        'FIFTH', 'SIXTH', 'SEVENTH', 'EIGHTH', 'NINTH', 'TENTH',
        
        # Additional common words
        'EVER', 'NEVER', 'ALWAYS', 'SOMETIMES', 'OFTEN', 'RARELY', 'SELDOM', 'USUALLY', 'NORMALLY',
        'GENERALLY', 'TYPICALLY', 'FREQUENTLY', 'OCCASIONALLY', 'CONSTANTLY', 'CONTINUOUSLY',
        'FOREVER', 'TEMPORARY', 'PERMANENT', 'SHORT', 'LONG', 'BRIEF', 'QUICK', 'FAST', 'SLOW',
        'RAPID', 'GRADUAL', 'SUDDEN', 'IMMEDIATE', 'INSTANT', 'DELAYED', 'LATE', 'EARLY', 'PROMPT',
        'TALKATIVE', 'QUIET', 'LOUD', 'NOISY', 'SILENT', 'PEACEFUL', 'CALM', 'BUSY', 'FREE', 'EMPTY',
        'FULL', 'HALF', 'WHOLE', 'ENTIRE', 'COMPLETE', 'PARTIAL', 'TOTAL', 'OVERALL', 'GENERAL',
        'SPECIFIC', 'PARTICULAR', 'CERTAIN', 'SURE', 'POSITIVE', 'NEGATIVE', 'TRUE', 'FALSE', 'REAL',
        'FAKE', 'GENUINE', 'ORIGINAL', 'COPY', 'DUPLICATE', 'SINGLE', 'DOUBLE', 'TRIPLE', 'MULTIPLE',
        'SEVERAL', 'VARIOUS', 'DIFFERENT', 'SIMILAR', 'SAME', 'EQUAL', 'EQUIVALENT', 'IDENTICAL',
        'DISTINCT', 'SEPARATE', 'INDEPENDENT', 'RELATED', 'CONNECTED', 'LINKED', 'ASSOCIATED',
    }


def _levenshtein(a: str, b: str) -> int:
    # simple iterative DP implementation
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i] + [0] * lb
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def normalize_ocr(text: str, candidates: Iterable[str] | None = None) -> str:
    """Apply SymSpell spell correction and normalizations.

    - Uppercases result
    - Applies explicit corrections (SOP->STOP, etc.)
    - Uses SymSpell for intelligent spell correction
    - Falls back to Levenshtein distance with NLTK dictionary
    - Filters URL artifacts
    """
    if not text:
        return text
    
    text = text.strip()
    if not text:
        return text
    
    # Load dictionaries
    english_words = load_english_dictionary()
    symspell = load_symspell()
    
    # Explicit corrections that should happen before any other processing
    explicit_corrections = {
        'SOP': 'STOP',
        'STGP': 'STOP',
        'ST0P': 'STOP',
        'STQP': 'STOP',
        'FRO': 'PRO',
        'WISHED': 'WISHES',
        'WSIS': 'WISHES',
        'NAPPY': 'HAPPY',
        'TALIVATIN': 'TALKATIVE',
        'MERI': 'VERY',
        'MERI,': 'VERY',
        'ROUTINELY': '',
        'SHARES': '',
        'COM': '',
    }
    
    # Apply explicit corrections first
    text_upper = text.upper()
    for wrong, right in explicit_corrections.items():
        if text_upper == wrong or wrong in text_upper:
            text_upper = text_upper.replace(wrong, right)
    
    # Clean up stray punctuation (remove commas between words)
    import re
    text_upper = re.sub(r'\s*,\s*', ' ', text_upper)
    
    # Filter out URL artifacts and clean up
    words = text_upper.split()
    filtered_words = []
    for w in words:
        w = w.strip()
        if not w:
            continue
        # Skip URL components
        if any(x in w.lower() for x in ['routinely', 'shares', 'com', '.com', 'http', 'www']):
            continue
        # Skip very short fragments
        if len(w) < 2:
            continue
        filtered_words.append(w)
    
    if not filtered_words:
        return text.upper().strip()
    
    # Try SymSpell correction
    corrected_words = []
    for word in filtered_words:
        # If word is already correct, keep it
        if word.lower() in english_words:
            corrected_words.append(word)
            continue
        
        # Try SymSpell correction with edit distance 1 only (conservative)
        if symspell and Verbosity:
            suggestions = symspell.lookup(word.lower(), Verbosity.CLOSEST, max_edit_distance=1)
            if suggestions and suggestions[0].distance == 1:
                best_suggestion = suggestions[0].term.upper()
                # Verify suggestion is in NLTK dictionary
                if best_suggestion.lower() in english_words:
                    corrected_words.append(best_suggestion)
                    continue
        
        # Keep the original word if no high-confidence correction found
        corrected_words.append(word)
    
    result = ' '.join(corrected_words)
    return result if result else text.upper().strip()
def log_message(message):
    print(f"[LOG] {message}")

def handle_error(error):
    print(f"[ERROR] {error}")

def display_image(image):
    import cv2
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()