### ai-bolitisp5

```
mkdir /root/scripts
cd /root/scripts
git clone https://github.com/ruslansvs2/ai-bolitisp5.git

echo '0 0 * * 3 root /root/scripts/ai-bolitisp5/update.ai-bolit.sh >> /dev/null 2>&1' >> /etc/crontab 
echo '0 1 * * 3 root /root/scripts/ai-bolitisp5/ai-bolitisp5.py >> /dev/null 2>&1' >> /etc/crontab


cd ai-bolitisp5

start check just one user
./ai-bolitisp5.py  user 

start check all of isp users 
./ai-bolitisp5.py 

``` 
