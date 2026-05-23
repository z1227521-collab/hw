# ---------------------------------------------------------------
# The Peace Game - SETUP FILE (Fixed Board Layout)
# ---------------------------------------------------------------

import json
import datetime
import random
import unicodedata

# The board - ALL POSITIVE peace-building activities!
board = [
    {"name": "Peace Summit",           "icon": "🏛️", "drop_min": 3,  "drop_max": 8,  "xp": 5,  "effect": "bonus_next"},
    {"name": "Embassy Reception",       "icon": "🏢", "drop_min": 5,  "drop_max": 10, "xp": 4,  "effect": "diplomacy"},
    {"name": "Global Collaboration",    "icon": "🌍", "drop_min": 2,  "drop_max": 12, "xp": 3,  "effect": "random_event"},
    {"name": "Reconciliation Talks",    "icon": "🤝", "drop_min": 4,  "drop_max": 11, "xp": 8,  "effect": "tension"},
    {"name": "Fair Trade Agreement",    "icon": "💼", "drop_min": 4,  "drop_max": 11, "xp": 4,  "effect": "economy"},
    {"name": "Humanitarian Aid",        "icon": "🎁", "drop_min": 5,  "drop_max": 9,  "xp": 7,  "effect": "crisis"},
    {"name": "Neutral Mediation",       "icon": "⚖️", "drop_min": 3,  "drop_max": 7,  "xp": 5,  "effect": "safe"},
    {"name": "Strategic Dialogue",      "icon": "🎙️", "drop_min": 4,  "drop_max": 9,  "xp": 4,  "effect": "alliance"},
    {"name": "Cultural Festival",       "icon": "🎭", "drop_min": 5,  "drop_max": 9,  "xp": 6,  "effect": "harmony"},
    {"name": "People-to-People Exchange","icon": "✈️", "drop_min": 4,  "drop_max": 8,  "xp": 5,  "effect": "harmony"},
    {"name": "Ceasefire Agreement",     "icon": "☮️", "drop_min": 5,  "drop_max": 10, "xp": 6,  "effect": "extra_turn"},
    {"name": "Resource Sharing Pact",   "icon": "💧", "drop_min": 4,  "drop_max": 9,  "xp": 7,  "effect": "steal"},
    {"name": "Joint Development Project","icon": "🏗️", "drop_min": 6,  "drop_max": 12, "xp": 6,  "effect": "economy"},
    {"name": "Historic Treaty",         "icon": "📜", "drop_min": 8,  "drop_max": 20, "xp": 9,  "effect": "major_breakthrough"},
    {"name": "Refugee Support Program", "icon": "🏕️", "drop_min": 5,  "drop_max": 10, "xp": 7,  "effect": "humanitarian"},
    {"name": "Truth & Reconciliation",  "icon": "🕯️", "drop_min": 6,  "drop_max": 12, "xp": 8,  "effect": "backfire"},
    {"name": "Crisis Hotline",          "icon": "📞", "drop_min": 4,  "drop_max": 8,  "xp": 5,  "effect": "communication"},
    {"name": "Diplomatic Mission",      "icon": "🚀", "drop_min": 5,  "drop_max": 10, "xp": 5,  "effect": "alliance"},
    {"name": "Education for Peace",     "icon": "📚", "drop_min": 4,  "drop_max": 9,  "xp": 8,  "effect": "warning"},
    {"name": "UN General Assembly",     "icon": "🇺🇳", "drop_min": 10, "drop_max": 18, "xp": 9,  "effect": "victory_boost"},
]

START_POSITION = 1
START_RISK     = 100
W              = 9
RECORDS_FILE   = "records.json"
XP_BONUS_THRESHOLD = 15

# ── Board geometry (defined before draw_board) ────────────────
full_divider = "+" + ("-" * W + "+") * 6
full_width   = len(full_divider)          # 61
middle_gap   = full_width - (2 * W) - 4  # 39
side_divider = "+" + "-" * W + "+" + " " * middle_gap + "+" + "-" * W + "+"

# Experience Milestones
MILESTONES = {
    40:  {"name": "Bridge Builder",    "desc": "Next landing gets +2-5 random bonus!"},
    80:  {"name": "Peace Ambassador",  "desc": "Permanent +1 to all future drops!"},
    130: {"name": "Harmony Champion",  "desc": "Permanent +2 to all drops!"},
    200: {"name": "Legend of Peace",   "desc": "Permanent +3 AND double XP gains!"},
}

# Positive random events
EVENTS = [
    {"name": "🌍 UN Peace Summit",          "effect": "all_players",    "value_min": 3,  "value_max": 8,  "desc": "Both gain random XP!"},
    {"name": "🕊️ Dove Release Ceremony",    "effect": "risk_down",      "value_min": 5,  "value_max": 12, "desc": "Risk drops!"},
    {"name": "🤝 Humanitarian Aid",          "effect": "current_player", "value_min": 5,  "value_max": 12, "desc": "Random boost next turn!"},
    {"name": "📰 Peace Media Campaign",      "effect": "both_players",   "value_min": 2,  "value_max": 6,  "desc": "Both gain random XP!"},
    {"name": "⚡ Crisis Resolved",           "effect": "risk_down",      "value_min": 8,  "value_max": 18, "desc": "Risk drops significantly!"},
    {"name": "🎓 Peace Academy Graduation",  "effect": "lowest_xp",      "value_min": 5,  "value_max": 12, "desc": "Lowest XP gains random amount!"},
    {"name": "💰 Debt Relief Program",       "effect": "risk_down",      "value_min": 4,  "value_max": 10, "desc": "Risk decreases!"},
    {"name": "🎲 Olympic Truce",             "effect": "random_player",  "value_min": 5,  "value_max": 15, "desc": "Random player gets big boost!"},
    {"name": "🌀 Diplomatic Breakthrough",   "effect": "risk_down",      "value_min": 6,  "value_max": 14, "desc": "Major risk reduction!"},
    {"name": "⭐ Nobel Peace Prize",         "effect": "current_player", "value_min": 8,  "value_max": 15, "desc": "Huge boost for current player!"},
    {"name": "🌱 Environmental Cooperation", "effect": "all_players",    "value_min": 4,  "value_max": 9,  "desc": "Both gain XP and risk drops!"},
    {"name": "🏥 Medical Aid Mission",       "effect": "risk_down",      "value_min": 5,  "value_max": 11, "desc": "Risk decreases!"},
]


# ---------------------------------------------------------------
# INTRODUCTION
# ---------------------------------------------------------------
def show_intro():
    print("=" * 55)
    print("         🕊️  THE PEACE GAME  🕊️")
    print("         (Positive Peace Edition)")
    print("=" * 55)
    print("\nWAR RISK: 100%. Build peace, one action at a time.")
    print("\n✨ ALL actions are positive peace-building activities!")
    print("🎲 No conflict. No weapons. Just hope and cooperation.")
    print("\nTwo players. One board. Only ONE winner.")
    print("\nType 'info' anytime. Press Enter to begin.\n")


# ---------------------------------------------------------------
# PLAYER SETUP
# ---------------------------------------------------------------
def setup_players():
    players = []
    print("\n👥 Name your peacemakers.\n")
    for n in [1, 2]:
        name = input(f"Player {n} name: ").strip() or f"Player{n}"
        players.append({
            "name": name, "token": name[0].upper(),
            "position": START_POSITION, "contributed": 0,
            "experience": 0, "combo": 0, "next_boost": 0,
            "permanent_bonus": 0, "last_turn_moved": False,
            "xp_multiplier": 1,
        })
    return players


# ---------------------------------------------------------------
# DROP HELPERS
# ---------------------------------------------------------------
def get_random_base_drop(space):
    return random.randint(space.get("drop_min", 3), space.get("drop_max", 8))


def calculate_actual_drop(base_drop, experience, permanent_bonus=0, next_boost=0):
    xp_bonus     = experience // XP_BONUS_THRESHOLD
    random_factor = random.randint(-1, 2)
    return max(1, base_drop + xp_bonus + permanent_bonus + next_boost + random_factor)


# ---------------------------------------------------------------
# SPACE EFFECTS
# ---------------------------------------------------------------
def apply_space_effect(space, player, other_player, risk, players):
    effect     = space.get("effect", "")
    message    = ""
    extra_drop = 0

    if effect == "bonus_next":
        bonus = random.randint(2, 6)
        player["next_boost"] += bonus
        message = f"✨ Momentum builds! +{bonus} boost for next action!"

    elif effect == "extra_turn":
        message = ("🔄 CEASEFIRE! Extra action granted!"
                   if random.random() < 0.7
                   else "⌛ Continuing the dialogue... no extra action this time.")

    elif effect == "steal":
        inspired = random.randint(2, 6)
        if other_player["experience"] >= inspired:
            other_player["experience"] -= inspired
            player["experience"]       += inspired
            message = f"💡 Your success inspired {other_player['name']} to share {inspired} XP!"
        else:
            player["experience"]       += 2
            other_player["experience"] += 2
            message = "🤝 Shared learning! Both gain 2 XP."

    elif effect == "tension":
        if risk > 50:
            extra_drop = random.randint(3, 8)
            message = f"⚖️ Difficult but productive talks! +{extra_drop} risk reduced!"

    elif effect == "crisis":
        if random.random() < 0.5:
            extra_drop = random.randint(3, 7)
            message = f"🎁 Emergency aid delivered! +{extra_drop} risk reduced!"
        else:
            message = "🤲 Communities come together to help!"

    elif effect == "backfire":
        roll       = random.randint(-3, 8)
        extra_drop = roll
        if roll > 0:
            message = f"🕯️ Healing begins! +{roll} risk reduced!"
        elif roll < 0:
            message = f"💔 Setback, but determination grows. Risk +{abs(roll)}."
        else:
            message = "🕊️ Small step forward."

    elif effect == "major_breakthrough":
        extra_drop = random.randint(6, 12)
        message = f"🏛️ HISTORIC BREAKTHROUGH! +{extra_drop} risk reduced!"

    elif effect == "victory_boost":
        player["permanent_bonus"] += 1
        message = "🌟 Global recognition! Permanent +1 to all future actions!"

    elif effect == "warning":
        if risk < 40:
            extra_drop = random.randint(3, 7)
            message = f"📚 Education initiative prevents future conflict! +{extra_drop}!"

    elif effect == "harmony":
        bonus = random.randint(1, 4)
        player["next_boost"]       += bonus
        other_player["next_boost"] += bonus
        message = f"🎵 Cultural harmony! Both gain +{bonus} boost!"

    elif effect == "economy":
        extra_drop = random.randint(3, 7)
        message = f"💼 Economic cooperation! +{extra_drop} risk reduced!"

    elif effect == "alliance":
        if random.random() < 0.5:
            player["permanent_bonus"] += 1
            message = "🤝 New strategic partnership! Permanent +1!"
        else:
            extra_drop = random.randint(4, 8)
            message = f"🤝 Alliance strengthens! +{extra_drop} risk reduced!"

    elif effect == "communication":
        extra_drop = random.randint(2, 5)
        message = f"📞 Open dialogue established! +{extra_drop} risk reduced!"

    elif effect == "humanitarian":
        extra_drop = random.randint(4, 9)
        message = f"🏕️ Humanitarian corridor opened! +{extra_drop} risk reduced!"

    elif effect == "safe":
        extra_drop = random.randint(2, 4)
        message = f"⚖️ Neutral ground for discussions! +{extra_drop}!"

    return extra_drop, message


# ---------------------------------------------------------------
# RANDOM EVENT
# ---------------------------------------------------------------
def trigger_random_event(players, risk, current_player):
    event = random.choice(EVENTS)
    value = random.randint(event["value_min"], event["value_max"])
    print(f"\n🌟 POSITIVE EVENT: {event['name']}")
    print(f"   {event['desc']} (Value: {value})")

    if event["effect"] == "all_players":
        for p in players:
            p["experience"] += value
        print(f"   → Both gain {value} XP!")
    elif event["effect"] == "risk_down":
        risk -= value
        print(f"   → Risk -{value}!")
    elif event["effect"] == "current_player":
        current_player["next_boost"] += value
        print(f"   → {current_player['name']} gains +{value} boost!")
    elif event["effect"] == "both_players":
        for p in players:
            p["experience"] += value
        print(f"   → Both gain {value} XP!")
    elif event["effect"] == "lowest_xp":
        lowest = min(players, key=lambda p: p["experience"])
        lowest["experience"] += value
        print(f"   → {lowest['name']} gains {value} XP!")
    elif event["effect"] == "random_player":
        target = random.choice(players)
        target["next_boost"] += value
        print(f"   → {target['name']} gets lucky! +{value} boost!")

    return risk


# ---------------------------------------------------------------
# MILESTONE CHECK
# ---------------------------------------------------------------
def check_milestones(player, old_xp):
    messages = []
    for milestone_xp, info in MILESTONES.items():
        if old_xp < milestone_xp <= player["experience"]:
            messages.append(f"🎉 {info['name']}! {info['desc']}")
            if milestone_xp == 40:
                bonus = random.randint(2, 5)
                player["next_boost"] += bonus
                messages.append(f"   → Random +{bonus} boost next action!")
            elif milestone_xp == 80:
                player["permanent_bonus"] += 1
                messages.append("   → Permanent +1 to all future actions!")
            elif milestone_xp == 130:
                player["permanent_bonus"] += 2
                messages.append("   → Permanent +2 to all future actions!")
            elif milestone_xp == 200:
                player["permanent_bonus"] += 3
                player["xp_multiplier"]    = 2
                messages.append("   → Permanent +3 AND double XP gains!")
    return messages


# ---------------------------------------------------------------
# INFO COMMAND
# ---------------------------------------------------------------
def show_info(risk, players):
    print("\n" + "-" * 40)
    print(f"📊 WAR RISK: {risk}%")
    print("-" * 40)
    for p in players:
        xp_bonus = p["experience"] // XP_BONUS_THRESHOLD
        print(f"\n{p['token']} {p['name']}:")
        print(f"   Risk reduced:     {p['contributed']}")
        print(f"   XP:               {p['experience']} (bonus +{xp_bonus})")
        print(f"   Permanent bonus:  +{p.get('permanent_bonus', 0)}")
        print(f"   Next action boost:+{p.get('next_boost', 0)}")
    print("-" * 40)


# ---------------------------------------------------------------
# EMOJI-AWARE CENTERING
# ---------------------------------------------------------------
def visual_len(text):
    """Return the visual column-width of a string (emoji = 2 cols).

    Regional indicator pairs (e.g. 🇺🇳) form a single flag glyph
    that renders as 2 columns — not 4 — so they are consumed in pairs.
    """
    width = 0
    chars = list(text)
    i = 0
    while i < len(chars):
        cp = ord(chars[i])
        # Skip variation selectors, ZWJ, combining enclosing keycap
        if cp in (0xFE0F, 0x200D, 0x20E3):
            i += 1
            continue
        # Regional indicator pair → one flag glyph = 2 cols
        if 0x1F1E0 <= cp <= 0x1F1FF:
            if i + 1 < len(chars) and 0x1F1E0 <= ord(chars[i + 1]) <= 0x1F1FF:
                width += 2
                i += 2          # consume both chars as one flag
            else:
                width += 2
                i += 1
            continue
        # All other emoji / symbol blocks = 2 cols
        if 0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF:
            width += 2
        else:
            eaw = unicodedata.east_asian_width(chars[i])
            width += 2 if eaw in ("W", "F") else 1
        i += 1
    return width


def vcenter(text, width):
    """Centre text in `width` columns, accounting for emoji visual width."""
    vw   = visual_len(text)
    pad  = max(0, width - vw)
    left = pad // 2
    return " " * left + text + " " * (pad - left)


# ---------------------------------------------------------------
# CELL HELPERS
# ---------------------------------------------------------------
def token_line(number, players):
    marks = [p["token"] for p in players if p["position"] == number]
    if not marks:
        return " " * W
    return f"[{' '.join(marks)}]".center(W)


def cell_lines(number, players):
    space  = board[number - 1]
    l_icon = vcenter(space["icon"], W)
    l_stat = f"{space['drop_min']}-{space['drop_max']}+{space['xp']}".center(W)
    l_tok  = token_line(number, players)
    return [l_icon, l_stat, l_tok, " " * W]   # always 4 rows


# ---------------------------------------------------------------
# BOARD DRAWING
# ---------------------------------------------------------------
def draw_board(players, risk):
    print()

    # ── top row: spaces 1-6 (left → right) ───────────────────
    print(full_divider)
    for row in range(4):                    # icon / stats / token / blank
        line = "|"
        for n in [1, 2, 3, 4, 5, 6]:
            line += cell_lines(n, players)[row] + "|"
        print(line)

    # ── middle: 20↔7  19↔8  18↔9  17↔10 ─────────────────────
    middle_text = [
        "   BUILDING  PEACE   ",
        f"   WAR RISK: {risk}%   ",
        "   Reach 0 to win!   ",
        "  Together we can!   ",
    ]
    pairs = [(20, 7), (19, 8), (18, 9), (17, 10)]

    print(full_divider)                     # top border of middle section
    for idx, (ln, rn) in enumerate(pairs):
        lc = cell_lines(ln, players)
        rc = cell_lines(rn, players)
        for row in range(4):
            if row == 1:
                text = middle_text[idx]
                pad  = (middle_gap - len(text)) // 2
                gap  = " " * pad + text + " " * (middle_gap - pad - len(text))
            else:
                gap = " " * middle_gap
            print(f"|{lc[row]}|{gap}|{rc[row]}|")
        if idx < 3:
            print(side_divider)             # divider between pairs (not after last)

    # ── bottom row: spaces 16-11 (right → left) ──────────────
    print(full_divider)                     # bottom border of middle section
    for row in range(4):                    # icon / stats / token / blank
        line = "|"
        for n in [16, 15, 14, 13, 12, 11]:
            line += cell_lines(n, players)[row] + "|"
        print(line)
    print(full_divider)


# ---------------------------------------------------------------
# LEGEND
# ---------------------------------------------------------------
def print_legend():
    print("\n" + "=" * 60)
    print("📖 MAP LEGEND (Icon → Peace Activity | Range | XP)")
    print("=" * 60)
    for i in range(0, 20, 2):
        left  = board[i]
        right = board[i + 1] if i + 1 < 20 else None
        left_str  = (f"  {left['icon']} #{i+1:2} {left['name'][:22]:22} "
                     f"{left['drop_min']:2}-{left['drop_max']:2} +{left['xp']:2}")
        right_str = (f"    {right['icon']} #{i+2:2} {right['name'][:22]:22} "
                     f"{right['drop_min']:2}-{right['drop_max']:2} +{right['xp']:2}"
                     if right else "")
        print(left_str + right_str)
    print("\n✨ All actions are positive peace-building activities!")
    print("=" * 60)


# ---------------------------------------------------------------
# CONTRIBUTIONS
# ---------------------------------------------------------------
def show_contributions(players):
    print("\n" + "-" * 40)
    print("🏆 PEACE CONTRIBUTIONS 🏆")
    for p in players:
        print(f"  {p['token']} {p['name']}: {p['contributed']} risk reduced "
              f"(XP: {p['experience']})")
    most    = max(p["contributed"] for p in players)
    winners = [p["name"] for p in players if p["contributed"] == most]
    if len(winners) == 1:
        print(f"\n🌟 Most Valuable Peacemaker: {winners[0]} ({most} risk reduced)!")
    else:
        print(f"\n🌟 TIE for MVP: {' & '.join(winners)}!")
    print("-" * 40)


# ---------------------------------------------------------------
# RECORDS
# ---------------------------------------------------------------
def load_records():
    try:
        with open(RECORDS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_record(winner, steps, players):
    records = load_records()
    records.append({
        "winner":  winner,
        "steps":   steps,
        "players": f"{players[0]['name']} & {players[1]['name']}",
        "date":    str(datetime.date.today()),
    })
    with open(RECORDS_FILE, "w") as f:
        json.dump(records, f)


def show_leaderboard():
    records = load_records()
    records.sort(key=lambda r: r["steps"])
    top = records[:5]
    print("\n" + "=" * 50)
    print("🏆 FASTEST PEACE RECORDS 🏆")
    print("=" * 50)
    if not top:
        print("  No records yet — play a game!")
    else:
        print(f"  {'#':<4} {'Peacemaker':<15} {'Steps':<8} {'Date':<12}")
        print("  " + "-" * 45)
        for i, r in enumerate(top, 1):
            print(f"  {i:<4} {r['winner']:<15} {r['steps']:<8} {r['date']:<12}")
        steps_list = [r["steps"] for r in top]
        if len(steps_list) > 1:
            print(f"\n  📊 Record spread: {min(steps_list)} to {max(steps_list)} steps")
    print("=" * 50)
