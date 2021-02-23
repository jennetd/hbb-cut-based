export EOS_MGM_URL=root://cmseos.fnal.gov

rm -r outfiles
eos cp -r /eos/uscms/store/user/jennetd/february-2021/inclusive/outfiles/ .

rm -r outdata
eos cp -r /eos/uscms/store/user/jennetd/february-2021/inclusive/outdata/ .
