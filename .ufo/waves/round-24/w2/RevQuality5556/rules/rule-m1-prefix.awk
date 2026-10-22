{ if (index($0, "PWD=" fleet)) sub(/PWD=[^;]*/, "PWD=inside-fleet-repo"); else sub(/PWD=[^;]*/, "PWD=outside-fleet-repo"); print }
