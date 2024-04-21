"""CLI usage of the API."""

if __package__ is None or len(__package__) <= 1:
    import sys
    from pathlib import Path

    DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(DIR.parent))
    __package__ = DIR.name

from .client import HydrocaptClient
from do_not_commit import USER, PASSWORD, POOL_INTERNAL_ID

if __name__ == "__main__":

    hc = HydrocaptClient(
        USER, PASSWORD, pool_internal_id=POOL_INTERNAL_ID
    )

    if hc.is_connection_ok() is False:
        print("BOOOOOOO")

    cmds_state = hc.get_commands_current_states()
    mesures = hc.get_pool_measure_latest()
    consigns_state = hc.get_current_consigns()
    all_data = hc.get_packaged_data()

    #datas = hc.fetch_all_data()

    hc.set_command_state("Light", "Pool Light OFF")


    hc.set_command_state("Filtration", "Filtration OFF")

    # hc.set_command_state_fast()

    c = hc.get_current_consigns()

    hc.set_consign(
        "Filtration Timer",
        [
            False,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ],
    )

    c = hc.get_current_consigns()

    hc.set_command_state("light", "Pool Light ON")

    hc.set_command_state("light", "Pool Light OFF")

    datas = hc.fetch_all_data()

    hc.set_command_state("light", "Pool Light ON")

    hc.set_command_state("light", "Pool Light OFF")

    datas = hc.fetch_all_data()
