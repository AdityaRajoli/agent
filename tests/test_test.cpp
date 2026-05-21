#include <gtest/gtest.h>

extern "C" {
    int find_max(int a, int b, int c);
}

TEST(AutoTest, Case1) { EXPECT_EQ(find_max(10, 5, 3),  10); }
TEST(AutoTest, Case2) { EXPECT_EQ(find_max(3, 9, 1),    9); }
TEST(AutoTest, Case3) { EXPECT_EQ(find_max(2, 4, 7),    7); }
TEST(AutoTest, Case4) { EXPECT_EQ(find_max(5, 5, 5),    5); }
TEST(AutoTest, Case5) { EXPECT_EQ(find_max(-1, -5, -10),-1); }
TEST(AutoTest, Case6) { EXPECT_EQ(find_max(0, 0, 1),    1); }
