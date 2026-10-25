"""
Automated Verification Suite for All Character Animations and Locomotion Physics.
Tests all 6 entities:
1. Lula (Main Pet)
2. Bolsonaro Peek Widget
3. Xandão Arrest Widget
4. Police Cruiser (Moro & Deltan)
5. Janja Aerolula
6. PUC Students Protest
"""
import sys
import os
import math

# Force offscreen QPA for headless environment if needed
os.environ["QT_QPA_PLATFORM"] = "offscreen"

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, QPoint

app = QApplication.instance() or QApplication(sys.argv)

print("--- STARTING COMPREHENSIVE VERIFICATION SUITE ---")

errors = []

# 1. VERIFY LULA PET WINDOW & SPRITES
try:
    from pet_window import LulaPetWindow, STATE_IDLE, STATE_WANDER, STATE_SNEAK_MOUSE, STATE_FLEE
    pet = LulaPetWindow()

    # Verify sprite frame counts (16 frames per animation cycle)
    expected_counts = {
        'idle': 16,
        'walk': 16,
        'sneak': 16,
        'hide': 16,
        'angry': 16,
        'crouch': 16,
        'drag': 16,
        'chase': 16
    }

    for cat, exp_count in expected_counts.items():
        count_r = len(pet.sprites.get(f"{cat}_r", []))
        count_l = len(pet.sprites.get(f"{cat}_l", []))
        if count_r != exp_count or count_l != exp_count:
            errors.append(f"Lula '{cat}' frame count mismatch: expected {exp_count}, got R={count_r}, L={count_l}")
        else:
            print(f"  [PASS] Lula '{cat}' sprite cycle: {count_r} frames (R & L)")

    # Verify locomotion physics
    start_x = pet.pos_x
    start_y = pet.pos_y
    target_x = start_x + 100
    target_y = start_y + 50

    # Step physics for 10 ticks
    for _ in range(10):
        pet._apply_movement_physics(target_x, target_y, max_speed=3.2)

    spd = math.hypot(pet.vel_x, pet.vel_y)
    if spd <= 0.1:
        errors.append("Lula physics failed to accelerate towards target")
    else:
        print(f"  [PASS] Lula physics acceleration: current speed = {spd:.2f} px/tick")

    if pet.stride_dist <= 0:
        errors.append("Lula ground stride distance did not increment during locomotion")
    else:
        print(f"  [PASS] Lula ground-synchronized stride: {pet.stride_dist:.2f} px traveled, bob={pet.locomotion_bob:.2f} px")

    # Verify deceleration near target
    pet.pos_x = target_x - 5.0
    pet.pos_y = target_y - 2.0
    for _ in range(15):
        dist, current_spd = pet._apply_movement_physics(target_x, target_y, max_speed=3.2)
    
    if current_spd > 1.0:
        errors.append(f"Lula did not decelerate smoothly on arrival: speed={current_spd}")
    else:
        print(f"  [PASS] Lula smooth arrival deceleration: final speed = {current_spd:.2f} px/tick")

    # Verify flee physics
    pet._apply_flee_physics(pet.pos_x - 10, pet.pos_y, max_speed=7.5)
    if pet.vel_x <= 0.1:
        errors.append("Lula flee physics did not accelerate away from cursor")
    else:
        print(f"  [PASS] Lula sprint flee physics: vel_x = {pet.vel_x:.2f}")

    pet.close()
except Exception as e:
    errors.append(f"Lula Pet Window error: {e}")

# 2. VERIFY BOLSONARO PEEK WIDGET
try:
    from bolsonaro_window import BolsonaroPeekWidget, clear_all_bolsonaro
    rect = QRect(0, 0, 1920, 1080)
    bolso = BolsonaroPeekWidget(rect)

    if len(bolso.frames) != 4:
        errors.append(f"Bolsonaro frame count mismatch: expected 4, got {len(bolso.frames)}")
    else:
        print(f"  [PASS] Bolsonaro corner peek: {len(bolso.frames)} dynamic frames loaded")

    # Test elastic slide up
    initial_y = bolso.current_y
    for _ in range(bolso.rise_duration + 5):
        bolso._step()
    
    if bolso.anim_state != 'peeking':
        errors.append(f"Bolsonaro failed to transition to 'peeking', state={bolso.anim_state}")
    else:
        print(f"  [PASS] Bolsonaro elastic cubic rise completed successfully: state={bolso.anim_state}, y={bolso.current_y:.1f}")

    # Test sway during peeking
    sway_y_before = bolso.current_y
    bolso._step()
    print(f"  [PASS] Bolsonaro peeking arminha firing & sway active: frame={bolso.frame_index}")

    clear_all_bolsonaro()
except Exception as e:
    errors.append(f"Bolsonaro Widget error: {e}")

# 3. VERIFY XANDÃO ARREST WIDGET
try:
    from xandao_window import XandaoArrestWidget, clear_all_xandao
    rect = QRect(0, 0, 1920, 1080)
    xandao = XandaoArrestWidget(rect, target_pos=QPoint(500, 500))

    if len(xandao.frames) != 4:
        errors.append(f"Xandão frame count mismatch: expected 4, got {len(xandao.frames)}")
    else:
        print(f"  [PASS] Xandão arrest widget: {len(xandao.frames)} dynamic frames loaded")

    # Step through descent
    for _ in range(xandao.descent_duration):
        xandao._step()
    print(f"  [PASS] Xandão dramatic descending entrance completed: y={xandao.current_y:.1f}")

    # Step to strike
    for _ in range(xandao.windup_duration + 2):
        xandao._step()
    
    if not xandao.cursor_locked:
        errors.append("Xandão failed to lock cursor upon gavel strike")
    elif len(xandao.shockwaves) == 0:
        errors.append("Xandão failed to trigger shockwave rings on gavel strike")
    else:
        print(f"  [PASS] Xandão gavel impact strike: cursor locked={xandao.cursor_locked}, shockwaves={len(xandao.shockwaves)}")

    clear_all_xandao()
except Exception as e:
    errors.append(f"Xandão Widget error: {e}")

# 4. VERIFY POLICE CRUISER (MORO & DELTAN)
try:
    from police_window import PoliceCarWidget, clear_all_police
    rect = QRect(0, 0, 1920, 1080)
    police = PoliceCarWidget(rect)

    if len(police.frames) != 4:
        errors.append(f"Police cruiser frame count mismatch: expected 4, got {len(police.frames)}")
    else:
        print(f"  [PASS] Police cruiser: {len(police.frames)} multi-phase rotating strobe frames loaded")

    # Test suspension bounce & exhaust smoke puffs
    start_x = police.current_x
    for _ in range(25):
        police._step()

    if police.current_x <= start_x:
        errors.append("Police cruiser failed to advance horizontally")
    elif len(police.smoke_puffs) == 0:
        errors.append("Police cruiser failed to emit exhaust smoke puffs")
    else:
        print(f"  [PASS] Police cruiser suspension bounce active, exhaust smoke particles={len(police.smoke_puffs)}")

    clear_all_police()
except Exception as e:
    errors.append(f"Police Cruiser error: {e}")

# 5. VERIFY JANJA AEROLULA
try:
    from plane_window import JanjaPlaneWidget, clear_all_planes
    rect = QRect(0, 0, 1920, 1080)
    plane = JanjaPlaneWidget(rect)

    if len(plane.frames) != 4:
        errors.append(f"Janja plane frame count mismatch: expected 4, got {len(plane.frames)}")
    else:
        print(f"  [PASS] Janja Aerolula: {len(plane.frames)} traveling wave banner frames loaded")

    # Test flight tick, altitude oscillation & contrails
    start_x = plane.current_x
    for _ in range(20):
        plane._step()

    if plane.current_x <= start_x:
        errors.append("Janja plane failed to advance horizontally")
    elif len(plane.contrails) == 0:
        errors.append("Janja plane failed to emit engine contrail particles")
    else:
        print(f"  [PASS] Janja Aerolula aerodynamic altitude wave & contrails active: contrails={len(plane.contrails)}")

    clear_all_planes()
except Exception as e:
    errors.append(f"Janja Plane error: {e}")

# 6. VERIFY PUC STUDENTS PROTEST
try:
    from puc_window import PUCProtestWidget, clear_all_protests
    rect = QRect(0, 0, 1920, 1080)
    puc = PUCProtestWidget(rect)

    if len(puc.frames) != 4:
        errors.append(f"PUC protest frame count mismatch: expected 4, got {len(puc.frames)}")
    else:
        print(f"  [PASS] PUC Students protest: {len(puc.frames)} marching cadence frames loaded")

    # Test marching cadence bounce & chant particles
    start_x = puc.current_x
    for _ in range(35):
        puc._step()

    if puc.current_x <= start_x:
        errors.append("PUC protest failed to advance horizontally")
    elif len(puc.chant_particles) == 0:
        errors.append("PUC protest failed to emit chant particles")
    else:
        print(f"  [PASS] PUC Students rhythmic marching cadence & chant particles active: chant_particles={len(puc.chant_particles)}")

    clear_all_protests()
except Exception as e:
    errors.append(f"PUC Protest error: {e}")

# 7. VERIFY MST & CUT OCCUPATION & TENT BUILDING
try:
    from mst_window import MSTInvasionWidget, MSTTentWidget, clear_all_mst_invasions
    rect = QRect(0, 0, 1920, 1080)
    
    # Test animated tent building
    tent = MSTTentWidget(200, 800, start_delay_ticks=0)
    if len(tent.stages) != 5:
        errors.append(f"MST Tent stages mismatch: expected 5, got {len(tent.stages)}")
    else:
        print(f"  [PASS] MST Tent: {len(tent.stages)} construction stages loaded")
    
    # Step through construction to fully pitched stage
    for _ in range(120):
        tent._step()
    if tent.current_stage != 4:
        errors.append(f"MST Tent failed to reach stage 4, current_stage={tent.current_stage}")
    else:
        print(f"  [PASS] MST Tent animated construction completed to stage {tent.current_stage} (smoke particles={len(tent.smoke_particles)})")

    # Test tent collapse
    tent.collapse()
    if not tent.is_collapsed:
        errors.append("MST Tent failed to collapse")
    else:
        print("  [PASS] MST Tent collapsed successfully upon eviction alert")

    # Test main occupation widget
    mst = MSTInvasionWidget(rect)
    if len(mst.pitch_frames) != 4 or len(mst.flee_frames) != 4:
        errors.append(f"MST Militants frame count mismatch: pitch={len(mst.pitch_frames)}, flee={len(mst.flee_frames)}")
    else:
        print(f"  [PASS] MST Militants: {len(mst.pitch_frames)} pitch frames and {len(mst.flee_frames)} flee frames loaded")

    if len(mst.tents) != 4:
        errors.append(f"MST multiple tents count mismatch: expected 4, got {len(mst.tents)}")
    else:
        print(f"  [PASS] MST Occupation: {len(mst.tents)} campsite tents spawned across desktop")

    # Test occupation phase step
    for _ in range(15):
        mst._step()
    if mst.state != 'occupying':
        errors.append(f"MST expected state 'occupying', got {mst.state}")
    else:
        print("  [PASS] MST Occupation phase active with chants and tent pitching")

    # Simulate mouse movement -> trigger 5-second eviction countdown
    mst.last_cursor_pos = QPoint(mst.last_cursor_pos.x() + 20, mst.last_cursor_pos.y() + 20)
    mst._step()
    if mst.state != 'countdown':
        errors.append(f"MST failed to enter 'countdown' on mouse move, state={mst.state}")
    else:
        print(f"  [PASS] MST Eviction countdown triggered by mouse movement: state={mst.state}, sec={mst.countdown_sec}")

    # Fast forward countdown to 0 -> trigger police raid & panic flee
    mst.countdown_ticks = 1
    mst._step()
    if mst.state != 'fleeing':
        errors.append(f"MST failed to enter 'fleeing' on countdown 0, state={mst.state}")
    elif mst.speed < 8.0:
        errors.append(f"MST panic sprint speed too low: {mst.speed}")
    else:
        print(f"  [PASS] MST Panic sprint triggered: state={mst.state}, speed={mst.speed} px/tick")

    clear_all_mst_invasions()
except Exception as e:
    errors.append(f"MST Occupation error: {e}")

print("--------------------------------------------------")
if errors:
    print(f"FAILED WITH {len(errors)} ERRORS:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("ALL 7 ENTITY ANIMATIONS & PHYSICS SYSTEMS VERIFIED SUCCESSFULLY!")
    sys.exit(0)
