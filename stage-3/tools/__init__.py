





from config import MODE

if MODE == "mock":
    from tools.mock.network_tools import (
        scan_network,
        grab_banner,
        check_rtsp,
        test_credentials
    )
else:
    from tools.real.network_tools import (
        scan_network,
        grab_banner,
        check_rtsp,
        test_credentials
    )