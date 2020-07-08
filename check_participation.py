from eth2fastspec import *
import os

state_path = 'my_state.ssz'
with open(state_path, 'rb') as f:
    state = BeaconState.deserialize(f, os.stat(state_path).st_size)

epc = EpochsContext()
epc.load_state(state)

process = prepare_epoch_process_state(epc, state)
att_marks = {
    'curr_head': FLAG_CURR_HEAD_ATTESTER,
    'curr_target': FLAG_CURR_TARGET_ATTESTER,
    'curr_source': FLAG_CURR_SOURCE_ATTESTER,
    'prev_head': FLAG_PREV_HEAD_ATTESTER,
    'prev_target': FLAG_PREV_TARGET_ATTESTER,
    'prev_source': FLAG_PREV_SOURCE_ATTESTER,
}

print(f'slot: {state.slot}')

def fmt_flag(flags: int) -> str:
    return '\t\t\t'.join([('y' if has_markers(flags, v) else 'n') for v in att_marks.values()])

print('index\tdelay\t'+'\t'.join(att_marks.keys()))

inactives = []
non_targets = []

for i, st in enumerate(process.statuses):
    if not st.active:
        print(f'{i}\t\t\tnot active')
        continue
    p = fmt_flag(st.flags)
    print(f'{i}\t\t\t{st.inclusion_delay}\t\t\t{p}')
    if 'y' not in p:
        inactives.append(i)
    if not (has_markers(st.flags, FLAG_CURR_TARGET_ATTESTER) or has_markers(st.flags, FLAG_PREV_TARGET_ATTESTER)):
        non_targets.append(i)

start_slot = compute_start_slot_at_epoch(get_previous_epoch(state))
end_slot = compute_start_slot_at_epoch(get_current_epoch(state)+1)
for slot in map(Slot, range(start_slot, end_slot)):
    comm_count = epc.get_committee_count_at_slot(slot)
    print(f"\n\n------- slot {slot} --------")
    for i in map(CommitteeIndex, range(comm_count)):
        comm = epc.get_beacon_committee(slot, i)
        print(f"slot {slot} committee {i}")
        print(f"  actives: {[i for i in comm if i not in inactives]}")
        print(f"  in-actives: {[i for i in comm if i in inactives]}")
        print("")

print("")
print("warning: if the state is not at the epoch boundary, some won't have attested yet")
print("")
print(f'inactives (count: {len(inactives)}):')
print(','.join(map(str, inactives)))

print('\n\n\n')
print(f'non-target voters (count: {len(non_targets)}):')
print(','.join(map(str, non_targets)))

print('done!')
