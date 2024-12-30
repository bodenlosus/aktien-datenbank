##!/usr/bin/env bash
mkdir -p /opt/aktiendb/
ln -sf $1 /opt/aktiendb/adb-update
cp -f .env /opt/aktiendb

cp -f aktiendb.service /etc/systemd/system
cp -f aktiendb.timer /etc/systemd/system

systemctl daemon-reload
systemctl enable aktiendb.timer
systemctl enable aktiendb.service
systemctl start aktiendb.timer