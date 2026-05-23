import random

from setup import (board, setup_players, show_info, draw_board, show_intro,
                   print_legend, save_record, show_leaderboard,
                   show_contributions, START_RISK, calculate_actual_drop,
                   XP_BONUS_THRESHOLD, apply_space_effect, trigger_random_event,
                   check_milestones, get_random_base_drop)


show_intro()
risk = START_RISK
players = setup_players()

draw_board(players, risk)
print_legend()

turn = 0
steps = 0
game_over = False

while not game_over:
    player = players[turn]
    other = players[1 - turn]
    
    print(f"\n{'='*50}")
    print(f"🎲 {player['name']}'s TURN")
    print(f"{'='*50}")
    
    #Show current stats
    xp_bonus = player["experience"] // XP_BONUS_THRESHOLD
    print(f"   XP: {player['experience']} (bonus +{xp_bonus})")
    if player.get("permanent_bonus", 0) > 0:
        print(f"   Permanent bonus: +{player['permanent_bonus']}")
    if player.get("next_boost", 0) > 0:
        print(f"   Next action boost: +{player['next_boost']}")
    
    #Info loop
    while True:
        choice = input("\nPress Enter to roll (or 'info'): ")
        if choice.lower() == "info":
            show_info(risk, players)
        else:
            break

    #Roll
    roll = random.randint(1, 6)
    steps += 1
    
    old_pos = player["position"]
    new_pos = ((old_pos - 1 + roll) % 20) + 1
    player["position"] = new_pos
    
    space = board[new_pos - 1]
    old_xp = player["experience"]
    
    #Get random base drop from the space's range
    base_drop = get_random_base_drop(space)
    
    #Calculate actual drop with all bonuses
    actual_drop = calculate_actual_drop(
        base_drop,
        player["experience"],
        player.get("permanent_bonus", 0),
        player.get("next_boost", 0)
    )
    
    #Reset next_boost after use
    player["next_boost"] = 0
    
    #Combo system
    if player.get("last_turn_moved", False):
        player["combo"] = player.get("combo", 0) + 1
        if player["combo"] >= 3:
            combo_bonus = 2
            actual_drop += combo_bonus
            print(f"\n🔥 {player['combo']} actions in a row! +{combo_bonus} bonus!")
    else:
        player["combo"] = 0
    
    #Space effect
    extra_drop, effect_msg = apply_space_effect(space, player, other, risk, players)
    actual_drop += extra_drop
    
    #Ensure drop is at least 1
    actual_drop = max(1, actual_drop)
    
    #Apply changes
    risk -= actual_drop
    player["contributed"] += actual_drop
    player["experience"] += space["xp"]
    
    #Milestones
    milestones = check_milestones(player, old_xp)
    
    #Random event (12% chance)
    if random.random() < 0.12:
        old_risk = risk
        risk = trigger_random_event(players, risk, player)
    
    #Display turn results
    print(f"\n🎲 Rolled a {roll}!")
    print(f"📍 Moved: {old_pos} → {new_pos}")
    print(f"🏛️ {space['name']} {space['icon']}")
    print(f"   Base reduction: {base_drop} (range {space['drop_min']}-{space['drop_max']})")
    
    #Bonus breakdown
    xp_bonus_used = old_xp // XP_BONUS_THRESHOLD
    bonuses = []
    if xp_bonus_used > 0:
        bonuses.append(f"XP +{xp_bonus_used}")
    if player.get("permanent_bonus", 0) > 0:
        bonuses.append(f"permanent +{player['permanent_bonus']}")
    if extra_drop > 0:
        bonuses.append(f"event +{extra_drop}")
    elif extra_drop < 0:
        bonuses.append(f"setback {extra_drop}")
    
    if bonuses:
        print(f"   Bonuses: {', '.join(bonuses)}")
    print(f"   💚 TOTAL risk reduced: {actual_drop}")
    print(f"   ⭐ Gained {space['xp']} XP (now {player['experience']})")
    
    if effect_msg:
        print(f"   {effect_msg}")
    for msg in milestones:
        print(f"   {msg}")
    
    print(f"\n📊 Remaining WAR RISK: {risk}%")
    draw_board(players, risk)
    
    #Check win
    if risk <= 0:
        print(f"\n{'🎉'*20}")
        print("*** PEACE SECURED! ***")
        print(f"{player['name']} WINS as the peacemaker!")
        print(f"Peace reached in {steps} moves!")
        print(f"{'🎉'*20}")
        show_contributions(players)
        save_record(player["name"], steps, players)
        show_leaderboard()
        game_over = True
    else:
        #Track last mover for combo
        for p in players:
            p["last_turn_moved"] = (p == player)
        
        #Extra turn check
        if space.get("effect") == "extra_turn" and random.random() < 0.7:
            print(f"\n🔄 {player['name']} gets an EXTRA ACTION!")
            #Don't switch turn
        else:
            turn = 1 - turn
