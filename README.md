# LAB02 - Tìm kiếm

## Mô tả

Đây là bài thực hành Lab02 môn Trí tuệ nhân tạo nâng cao, tập trung vào
việc tìm hiểu các phương pháp giải quyết bài toán bằng tìm kiếm. Nội dung
thực hành bao gồm tìm kiếm trên cây, tìm kiếm trong mê cung, so sánh BFS,
DFS và A*, kiểm tra chu trình, cũng như ảnh hưởng của các heuristic.

## Tài liệu yêu cầu

File yêu cầu của bài tập: https://classroom.google.com/w/ODg0NjkxMTA1OTQ3/t/all

## Cấu trúc thư mục

```
LAB02_SEARCHING/
├── src/
│   ├── 01_trees.ipynb
│   ├── 02_Maze_Example.ipynb
│   ├── 03_Maze_Example_Animation.ipynb
│   ├── 04_Maze_BFS_vs_A_Star.ipynb
│   ├── 05_Maze_Example-Animation_Cycle_checking.ipynb
│   ├── 06_Explore_heuristics.ipynb
│   ├── Ex1_Maze.ipynb
│   ├── Ex2_Maze_simplified.ipynb
│   ├── Ex3_Show_all_mazes.ipynb
│   ├── maze_helper.py
│   ├── tree_search_solution.py
│   └── *.txt
├── baocao.docx
└── README.md
```

### Mô tả các thành phần

- `src/01_trees.ipynb`: Thực hành tìm kiếm trên cây.
- `src/02_Maze_Example.ipynb`: So sánh không gian trạng thái được duyệt
  trong bài toán mê cung.
- `src/03_Maze_Example_Animation.ipynb`: Minh họa bằng animation quá trình
  tìm kiếm của BFS, DFS và A*.
- `src/04_Maze_BFS_vs_A_Star.ipynb`: So sánh BFS và A* trên mê cung.
- `src/05_Maze_Example-Animation_Cycle_checking.ipynb`: Minh họa vấn đề
  chu trình trong tìm kiếm và cách kiểm tra chu trình.
- `src/06_Explore_heuristics.ipynb`: Khảo sát ảnh hưởng của các heuristic.
- `src/Ex1_Maze.ipynb`: Bài tập giải mê cung bằng tác tử lập kế hoạch
  hướng mục tiêu.
- `src/Ex2_Maze_simplified.ipynb`: Bài tập mê cung rút gọn sử dụng BFS.
- `src/Ex3_Show_all_mazes.ipynb`: Hiển thị các mê cung dùng trong bài tập.
- `src/maze_helper.py`: Các hàm hỗ trợ đọc, hiển thị và thao tác với mê cung.
- `src/tree_search_solution.py`: Mã nguồn hỗ trợ cho bài toán tìm kiếm trên
  cây.
- `src/*.txt`: Dữ liệu đầu vào, gồm các mê cung với kích thước và cấu trúc
  khác nhau.
- `baocao.docx`: File báo cáo của bài thực hành.
- `README.md`: Tài liệu giới thiệu và hướng dẫn tổng quan cho repository.