#!/bin/sh

bs=0
while read -r t ; do
    if [ "$bs" -eq 1 ] ; then
        if [ "a$t" = "aend" ] ; then
            bs=2
        else
            set $(printf "%d " "'$(echo $t | cut -c1)" "'$(echo $t | cut -c2)" "'$(echo $t | cut -c3)" "'$(echo $t | cut -c4)" "'$(echo $t | cut -c5)" "'$(echo $t | cut -c6)" "'$(echo $t | cut -c7)" "'$(echo $t | cut -c8)" "'$(echo $t | cut -c9)" "'$(echo $t | cut -c10)" "'$(echo $t | cut -c11)" "'$(echo $t | cut -c12)" "'$(echo $t | cut -c13)" "'$(echo $t | cut -c14)" "'$(echo $t | cut -c15)" "'$(echo $t | cut -c16)" "'$(echo $t | cut -c17)" "'$(echo $t | cut -c18)" "'$(echo $t | cut -c19)" "'$(echo $t | cut -c20)" "'$(echo $t | cut -c21)" "'$(echo $t | cut -c22)" "'$(echo $t | cut -c23)" "'$(echo $t | cut -c24)" "'$(echo $t | cut -c25)" "'$(echo $t | cut -c26)" "'$(echo $t | cut -c27)" "'$(echo $t | cut -c28)" "'$(echo $t | cut -c29)" "'$(echo $t | cut -c30)" "'$(echo $t | cut -c31)" "'$(echo $t | cut -c32)" "'$(echo $t | cut -c33)" "'$(echo $t | cut -c34)" "'$(echo $t | cut -c35)" "'$(echo $t | cut -c36)" "'$(echo $t | cut -c37)" "'$(echo $t | cut -c38)" "'$(echo $t | cut -c39)" "'$(echo $t | cut -c40)" "'$(echo $t | cut -c41)" "'$(echo $t | cut -c42)" "'$(echo $t | cut -c43)" "'$(echo $t | cut -c44)" "'$(echo $t | cut -c45)" "'$(echo $t | cut -c46)" "'$(echo $t | cut -c47)" "'$(echo $t | cut -c48)" "'$(echo $t | cut -c49)" "'$(echo $t | cut -c50)" "'$(echo $t | cut -c51)" "'$(echo $t | cut -c52)" "'$(echo $t | cut -c53)" "'$(echo $t | cut -c54)" "'$(echo $t | cut -c55)" "'$(echo $t | cut -c56)" "'$(echo $t | cut -c57)" "'$(echo $t | cut -c58)" "'$(echo $t | cut -c59)" "'$(echo $t | cut -c60)" "'$(echo $t | cut -c61)")
            l=$(($1 -32 & 63 ))
            shift
            while [ $l -gt 0 ] ; do
                i0=$(($1 -32 & 63))
                shift
                i1=$(($1 -32 & 63))
                shift
                i2=$(($1 -32 & 63))
                shift
                i3=$(($1 -32 & 63))
                shift
                if [ $l -gt 2 ] ; then
                    echo -ne "\0$(($i0 >> 4))$(($i0 >> 1 & 7))$(($i0 << 2 & 4 | $i1 >> 4))\0$(($i1 >> 2 & 3))$(($i1 << 1 & 6 | $i2 >> 5))$(($i2 >> 2 & 7))\0$(($i2 & 3))$(($i3 >> 3 & 7))$(($i3 & 7))"
                    true
                elif [ $l -eq 2 ] ; then
                    echo -ne "\0$(($i0 >> 4))$(($i0 >> 1 & 7))$(($i0 << 2 & 4 | $i1 >> 4))\0$(($i1 >> 2 & 3))$(($i1 << 1 & 6 | $i2 >> 5))$(($i2 >> 2 & 7))"
                    true
                else
                    echo -ne "\0$(($i0 >> 4))$(($i0 >> 1 & 7))$(($i0 << 2 & 4 | $i1 >> 4))"
                    true
                fi
                l=$(($l-3))
            done
        fi
    elif [ $(echo $t | cut -c1-5) = "begin" ]; then
        bs=1
    fi
done