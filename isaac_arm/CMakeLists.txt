cmake_minimum_required(VERSION 3.8)
project(isaac_arm)

# --- 編譯器選項（C++ 時才會用到，可保留） ---
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# --- 尋找必要套件 ---
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)  # 🔹 加這行才能支援 Python 安裝

# --- 安裝 Python 套件 ---
ament_python_install_package(src)

# --- 安裝 Python 節點到 lib/${PROJECT_NAME}/ ---
install(
  PROGRAMS
    src/joint_keyboard_control.py       # 🔹 你的 Python 節點檔案
  DESTINATION lib/${PROJECT_NAME}
)

# --- 測試區域（可保留不動） ---
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

