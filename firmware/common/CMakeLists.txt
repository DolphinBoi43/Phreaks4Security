add_library(common STATIC
  crc16.c
  frame.c
)

target_include_directories(common PUBLIC
  ${CMAKE_CURRENT_SOURCE_DIR}
)
