cd boostedhiggs/
rm boostedhiggs.tar.gz boostedhiggs/*~
tar -zcvf boostedhiggs.tar.gz boostedhiggs --exclude __pycache__
cp boostedhiggs.tar.gz ../
cd ../
