{
  "Description": "Un plugin de Docker CLI para funcionalidades de Docker Scout.",
  "Documentation": "https://narutosi77.github.io/scout-cli/", # Tu URL de docs
  "Vendor": "narutosi77",
  "Version": "1.0.0",
  "Interface": {
    "Types": [
      "docker.api.Plugin"
    ],
    "Socket": "plugin.sock"
  },
  "Mounts": [
    {
      "Name": "data",
      "Source": "/var/lib/docker/plugins/my-scout-plugin",
      "Destination": "/data",
      "Options": ["bind"]
    }
  ],
  "Env": [
    {
      "Name": "DEBUG",
      "Description": "Habilita la depuración detallada",
      "Settable": ["value"],
      "Value": "false"
    }
  ],
  "Args": {
    "Name": "",
    "Description": ""
  },
  "Linux": {
    "Capabilities": ["CAP_NET_BIND_SERVICE"],
    "AllowAllDevices": false,
    "Devices": [],
    "Privileged": false
  },
  "User": {}
}