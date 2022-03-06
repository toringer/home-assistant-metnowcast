[![home-assistant-metnowcast](https://img.shields.io/github/release/toringer/home-assistant-metnowcast.svg?1)](https://github.com/toringer/home-assistant-metnowcast)
[![Validate with hassfest](https://github.com/toringer/home-assistant-metnowcast/workflows/Validate%20with%20hassfest/badge.svg)](https://github.com/toringer/home-assistant-metnowcast/actions/workflows/hassfest.yaml)
[![HACS Validation](https://github.com/toringer/home-assistant-metnowcast/actions/workflows/validate_hacs.yaml/badge.svg)](https://github.com/toringer/home-assistant-metnowcast/actions/workflows/validate_hacs.yaml)
[![Maintenance](https://img.shields.io/maintenance/yes/2022.svg)](https://github.com/toringer/home-assistant-metnowcast)
[![home-assistant-metnowcast_downloads](https://img.shields.io/github/downloads/toringer/home-assistant-metnowcast/total)](https://github.com/toringer/home-assistant-metnowcast)
[![home-assistant-metnowcast_downloads](https://img.shields.io/github/downloads/toringer/home-assistant-metnowcast/latest/total)](https://github.com/toringer/home-assistant-metnowcast)

# Met.no Nowcast component

Add precipitation nowcast to your Home Assistant. This component will add a weather sensor with data from the [met.no](https://www.met.no/) precipitation [nowcast](https://api.met.no/weatherapi/nowcast/2.0/documentation) service.

The weather sensor holds precipitation data for the next 90 minutes. Detailed precipitation data is available in the `forecast` attribute.

Only available for locations in the Nordic area.

## Installation

- Ensure that [HACS](https://hacs.xyz/) is installed.
- In HACS / Integrations / menu / Custom repositories, add the url the this repository.
- Search for and install the Met.no Nowcast integration.
- Restart Home Assistant.

## Configuration

Configuration of the integration is done through Configuration > Integrations where you enter coordinates.
