5 rem taken from https://nickm.com/post/2010/07/one-line-c64-basic-music/comment-page-1/
10 poke 54272+int(rnd(1) *25),int(rnd(1) *256) : goto 10
20 rem by Nick Montfort