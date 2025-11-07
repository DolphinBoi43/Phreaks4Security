add_executable(mcu_b
  src/main.c
)

target_include_directories(mcu_b PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  ${CMAKE_SOURCE_DIR}/firmware/common
)

target_link_libraries(mcu_b PRIVATE common)
