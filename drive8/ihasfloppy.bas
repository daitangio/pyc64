0 rem --- ihasfloppy by genesis project ---
1 rem --- see http://csdb.dk/release/?id=122467 ---
9 rem
10 poke 53280,0: poke 53281,0: restore
20 for i=0 to 999
30 read c: poke 1024+i, c
40 next i
50 for i=0 to 999
60 read c: poke 55296+i, c
70 next i
80 sleep 4
999 rem --- character screen data ---
1000 data 32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,233,205,32,32,32,32,32,32,32,32,32,32,32,32,32,32
1001 data 32,32,32,32,65,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,233,205,205,227,205,105,32,32,32,32,32,32,32,32,32,32,32,32,32,32
1002 data 32,32,32,32,206,231,223,32,32,32,32,32,32,32,32,32,32,32,233,205,160,231,231,160,105,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32
1003 data 32,32,32,32,95,206,167,205,227,205,223,32,85,104,98,248,247,227,105,87,95,105,99,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32
1004 data 32,32,32,32,32,99,95,231,160,231,160,227,28,87,233,105,83,119,99,95,239,100,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32
1005 data 32,32,32,32,32,32,32,99,95,206,228,239,210,192,196,32,32,32,32,32,186,162,102,68,73,32,32,111,111,111,111,111,111,111,111,111,111,32,32,32
1006 data 32,32,32,32,32,32,32,32,32,32,100,230,162,186,174,223,73,32,85,233,167,160,105,41,32,32,103,32,98,98,98,98,98,32,32,32,122,32,32,32
1007 data 32,32,32,32,32,32,32,32,32,39,40,95,160,160,167,174,186,227,186,236,119,104,32,32,32,32,103,32,227,227,227,227,227,32,32,32,80,44,32,32
1008 data 32,32,32,32,32,32,32,32,32,32,32,103,104,95,239,160,105,119,83,32,32,105,32,32,32,32,89,32,69,69,69,69,69,32,32,100,89,201,223,32
1009 data 32,32,32,32,32,32,32,32,32,32,32,32,95,32,32,83,32,32,32,32,32,32,32,32,32,32,89,32,32,32,85,69,73,32,233,160,160,160,187,32
1010 data 32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,72,32,32,32,84,32,89,32,188,160,160,160,105,32
1011 data 32,32,32,32,32,32,32,32,32,32,32,32,32,33,32,32,32,32,32,32,32,32,32,32,32,32,66,32,32,32,74,82,75,32,95,160,228,206,32,32
1012 data 32,32,32,32,32,32,32,32,32,32,32,32,100,100,32,32,32,32,32,59,32,32,32,32,32,32,71,32,32,32,85,73,32,87,233,247,227,167,101,32
1013 data 32,32,32,32,32,32,32,32,32,32,233,239,198,198,239,223,32,32,32,92,32,32,32,32,32,32,84,32,32,32,66,66,32,32,95,169,160,105,32,32
1014 data 32,32,32,32,32,32,32,32,32,233,206,174,105,32,95,102,32,32,32,33,32,32,32,32,32,32,101,32,32,32,74,75,32,32,32,99,101,32,32,32
1015 data 32,32,32,32,32,32,32,32,32,206,160,105,32,33,32,39,92,32,32,103,32,32,32,32,32,32,76,111,82,82,70,70,64,68,69,119,32,32,32,32
1016 data 32,32,32,32,32,32,32,32,32,32,99,32,32,39,92,32,33,32,32,32,92,32,32,32,32,32,32,32,32,32,32,245,162,105,32,32,32,32,32,32
1017 data 32,32,32,32,32,32,32,32,32,32,32,32,32,32,252,233,32,44,32,65,41,32,32,32,32,32,32,32,32,32,32,229,160,73,32,32,32,32,32,32
1018 data 32,32,32,32,32,32,32,32,32,32,32,32,32,32,95,197,98,192,98,197,172,73,32,32,32,32,32,32,32,32,32,160,105,40,32,32,32,32,32,32
1019 data 32,32,32,32,32,32,32,32,32,32,32,32,32,32,28,95,197,196,196,197,92,32,32,32,32,32,32,32,32,32,103,160,75,32,32,32,32,32,32,32
1020 data 32,32,32,32,32,32,32,32,32,32,32,32,32,103,92,39,40,34,34,39,32,32,32,32,32,32,32,32,32,32,118,160,68,73,32,32,32,32,32,32
1021 data 32,32,32,32,32,32,32,32,32,32,32,32,32,103,223,32,32,32,233,84,104,32,32,32,32,32,32,32,44,233,202,160,73,32,32,32,32,32,32,32
1022 data 32,32,32,32,32,32,32,32,32,32,32,32,85,69,95,247,248,247,105,32,160,223,44,32,32,32,85,233,162,160,105,40,32,32,32,32,32,32,32,32
1023 data 32,32,32,32,32,32,32,32,32,32,32,233,186,162,223,119,120,119,32,233,205,160,252,44,104,230,162,160,236,34,32,32,32,32,32,32,32,32,240,64
1024 data 32,32,32,32,32,32,32,32,32,32,108,232,228,232,228,223,98,248,247,228,167,229,172,174,228,172,232,105,41,32,32,32,32,32,32,32,32,32,32,120
1999 rem -- color data --
2000 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,12,11,14,14,14,14,14,14,14,14,14,14,14,14,14,14
2001 data 14,14,14,14,15,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,15,15,15,12,11,11,14,14,14,14,14,14,14,14,14,14,14,14,14,14
2002 data 14,14,14,14,15,15,12,14,14,14,14,14,14,14,14,14,14,14,12,15,15,12,11,11,11,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14
2003 data 14,14,14,14,11,12,12,12,1,1,15,14,14,14,14,14,14,14,14,13,11,11,11,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14
2004 data 14,14,14,14,14,11,11,11,12,12,15,12,14,1,14,14,3,3,3,6,6,6,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14
2005 data 14,14,14,14,14,14,14,11,11,11,11,11,14,14,14,14,14,14,14,14,6,6,6,11,11,14,14,12,12,12,12,12,12,12,12,12,12,14,14,14
2006 data 14,14,14,14,14,14,14,14,14,14,11,14,14,14,14,14,14,14,6,6,6,6,6,11,14,14,11,14,15,15,15,15,15,14,14,14,11,14,14,14
2007 data 14,14,14,14,14,14,14,14,14,11,11,14,14,14,14,14,14,14,6,6,6,2,14,14,14,14,11,14,15,15,15,15,15,14,14,14,11,14,14,14
2008 data 14,14,14,14,14,14,14,14,14,14,14,4,4,14,14,14,14,6,15,14,14,15,14,14,14,14,11,14,15,15,15,15,15,14,14,6,11,14,14,14
2009 data 14,14,14,14,14,14,14,14,14,14,14,14,1,14,14,15,14,14,14,14,14,14,14,14,14,14,11,14,14,14,11,11,11,14,6,6,6,6,6,14
2010 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,11,14,14,14,11,14,11,14,6,6,6,6,6,14
2011 data 14,14,14,14,14,14,14,14,14,14,14,14,14,6,14,14,14,14,14,14,14,14,14,14,14,14,11,14,14,14,11,11,11,14,6,6,6,6,14,14
2012 data 14,14,14,14,14,14,14,14,14,14,14,2,2,2,14,14,14,14,14,6,14,14,14,14,14,14,11,14,14,14,11,11,14,11,6,6,6,6,6,14
2013 data 14,14,14,14,14,14,14,14,14,14,2,2,2,2,2,2,14,14,14,6,14,14,14,14,14,14,11,14,14,14,11,11,14,14,6,6,6,6,14,14
2014 data 14,14,14,14,14,14,14,14,14,2,2,2,2,14,2,2,2,14,14,9,14,14,14,14,14,14,11,14,14,14,11,11,14,14,14,6,11,14,14,14
2015 data 14,14,14,14,14,14,14,14,2,2,2,2,14,6,14,2,2,14,14,2,14,14,14,14,14,14,11,11,11,11,11,11,11,11,11,11,14,14,14,14
2016 data 14,14,14,14,14,14,14,14,14,14,2,2,14,6,6,14,2,14,14,14,2,14,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14
2017 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,4,15,14,12,14,10,2,14,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14
2018 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14
2019 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14,14,14,14,6,6,6,14,14,14,14,14,14,14
2020 data 14,14,14,14,14,14,14,14,14,14,14,14,14,6,14,6,6,6,6,6,14,14,14,14,14,14,14,14,14,14,6,6,6,6,14,14,14,14,14,14
2021 data 14,14,14,14,14,14,14,14,14,14,14,14,14,6,14,14,14,14,6,6,6,14,14,14,14,14,14,14,6,6,6,6,6,14,14,14,14,14,14,14
2022 data 14,14,14,14,14,14,14,14,14,14,14,14,6,6,14,6,6,6,6,14,6,6,6,14,14,14,6,6,6,6,6,6,14,14,14,14,14,14,14,14
2023 data 14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,6,6,6,14,6,6,6,6,6,6,6,6,6,6,6,14,14,14,14,14,14,14,14,6,6
2024 data 14,14,14,14,14,14,14,14,14,14,6,14,14,14,14,14,6,6,6,6,6,6,6,6,6,6,6,6,6,14,14,14,14,14,14,14,14,14,14,6