# Naming Convention

1. 每个 Chapter 作为单独文件夹

2. 若 Chapter 内有子分类则每个子文件夹命名为：

   `Chapter{chapter_id}.{section_id}_{question_id}`

   文件命名为：

   `Chapter{chapter_id}.{section_id}`

   e.g. 第五章，第（一）部分，第一个问题处在

   ``` css
   Data
   └── Chapter5
       └── Chapter5.1
           └── Chapter5.1_1.md
   
   ```

   

   :dart:注意：`_` 之后一定为问题号