gh cache list -R bodenlosus/aktien-datenbank | awk '$5 < "2100-11-28"' | cut -f2 | xargs -I {} gh cache delete -R bodenlosus/aktien-datenbank {}
