# CMake generated Testfile for 
# Source directory: /home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/src/hash
# Build directory: /home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/debug/hash
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(test-hash[valgrind] "/usr/bin/valgrind" "--leak-check=full" "--quiet" "--error-exitcode=1" "./test-hash")
set_tests_properties(test-hash[valgrind] PROPERTIES  _BACKTRACE_TRIPLES "/home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/src/hash/CMakeLists.txt;62;add_test;/home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/src/hash/CMakeLists.txt;0;")
add_test(test-hash[normal] "./test-hash")
set_tests_properties(test-hash[normal] PROPERTIES  _BACKTRACE_TRIPLES "/home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/src/hash/CMakeLists.txt;64;add_test;/home/henry/Bureau/L3/S5/Structures de données - avancé_20250915_1543/TP-hash-etudiants/TP-hash-etudiants/src/hash/CMakeLists.txt;0;")
