include(GUDHI_boost_test)

add_executable_with_targets(Persistent_cohomology_test_unit persistent_cohomology_unit_test.cpp TBB::tbb)
add_executable_with_targets(Persistent_cohomology_test_betti_numbers betti_numbers_unit_test.cpp TBB::tbb)

# Do not forget to copy test results files in current binary dir
file(COPY "${CMAKE_SOURCE_DIR}/src/Persistent_cohomology/test/simplex_tree_file_for_unit_test.txt"
     DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/)

# Unitary tests
gudhi_add_boost_test(Persistent_cohomology_test_unit)
gudhi_add_boost_test(Persistent_cohomology_test_betti_numbers)

if(GMPXX_FOUND AND GMP_FOUND)
  add_executable ( Persistent_cohomology_test_unit_multi_field persistent_cohomology_unit_test_multi_field.cpp )
  target_link_libraries(Persistent_cohomology_test_unit_multi_field ${GMPXX_LIBRARIES} ${GMP_LIBRARIES})
  if(TARGET TBB::tbb)
    target_link_libraries(Persistent_cohomology_test_unit_multi_field TBB::tbb)
  endif()

  # Do not forget to copy test results files in current binary dir
  file(COPY "${CMAKE_SOURCE_DIR}/src/Persistent_cohomology/test/simplex_tree_file_for_multi_field_unit_test.txt"
       DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/)
  # Unitary tests
  gudhi_add_boost_test(Persistent_cohomology_test_unit_multi_field)

endif(GMPXX_FOUND AND GMP_FOUND)
