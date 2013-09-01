#Assuming input is $FILE

#If CR is used:
tr "\r" "\n" <$FILE
# (Octal for carriage return is 012)

#If CRLF is used:
tr -d "\r" <$FILE
# (Octal for carriage return is 015)

#Replace ";" with ",":
tr ";" "," <$FILE
# (Octal for semi-colon is 073 and colon is 054)

#It can be done with Perl as well:
perl -pe "s/\;/\,/g" $FILE
perl -pe "s/\r?\n|\r/\n/g" $FILE