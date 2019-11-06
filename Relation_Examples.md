# Relations

The character `*` means `UNIQUE`

# One To Many (Many to One)

### Authors

| id\* |    full_name\*     |
| :--: | :----------------: |
|  1   |    Brian Tracy     |
|  2   | Robert T. Kiyosaki |
|  3   |    Rolf Dobelli    |
|  4   |    Jane Austen     |

### Books

| id\* |            book_name             | author_id (`authors.id`) |
| :--: | :------------------------------: | :----------------------: |
|  1   |     The Art of the Good Life     |            3             |
|  2   |        Rich Dad, Poor Dad        |            2             |
|  3   |         Time Management          |            1             |
|  4   |       Pride and Prejudice        |            4             |
|  5   | The Business of the 21st Century |            2             |
|  6   |      Sense and Sensibility       |            4             |
|  7   |               Emma               |            4             |
|  8   |  The Psychology of Achievement   |            1             |

# One To One

### Teachers

| id\* |  full_name\*  |
| :--: | :-----------: |
|  1   |   John Doe    |
|  2   | Dudley Taylan |
|  3   | Jamal Detrick |
|  4   | Fannie Warntz |

### Classes

| id\* |  name  | teacher_id\* |
| :--: | :----: | :----------: |
|  1   |  ABC   |      3       |
|  2   |  DEF   |      4       |
|  3   | QWERTY |      2       |
|  4   | ASDFGH |      1       |

# Many to Many

### Categories

| id\* | category_name\* |
| :--: | :-------------: |
|  1   |   Programming   |
|  2   |      Media      |
|  3   |    Graphics     |
|  4   |      News       |

### Posts

| id\* |                title                 |
| :--: | :----------------------------------: |
|  1   |          How to use Flask?           |
|  2   |    Python's author is resigning!!    |
|  3   |       Uploading Media on Flask       |
|  4   | Version Control System for Designers |

### Posts_Categories (Association Table)

**`post_id` + `category_id` should be unique next to each other!!***

| post_id | category_id |
| :-----: | :---------: |
|    1    |      1      |
|    2    |      1      |
|    2    |      4      |
|    3    |      1      |
|    3    |      2      |
|    4    |      3      |
