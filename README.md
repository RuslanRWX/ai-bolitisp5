# ai-bolitisp5

echo '0	0 * * 3 root /root/scripts/ai-bolitisp5/update.ai-bolit.sh >> /dev/null 2>&1' >> /etc/crontab 
echo '0	1 * * 3 root /root/scripts/ai-bolitisp5/ai-bolitisp5.py >> /dev/null 2>&1' >> /etc/crontab 
