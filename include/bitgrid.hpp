#pragma once

#include <array>
#include <cstdint>

template<std::size_t W, std::size_t H>
class BitGrid
{
    std::array<uint8_t, (W * H + 7)/8> grid;
public:
    bool get(int x, int y);
    void set(int x, int y, bool val);
    constexpr size_t width() const { return W; }
    constexpr size_t height() const { return H; }
};

template<std::size_t W, std::size_t H>
bool BitGrid<W, H>::get(int x, int y)
{
    int index = y*W+x;
    int byte_num = index / 8;
    int bit_offset = index % 8;
    return (this->grid[byte_num] >> bit_offset ) & 1;
}

template<std::size_t W, std::size_t H>
void BitGrid<W, H>::set(int x, int y, bool val)
{
    int index = y*W+x;
    int byte_num = index / 8;
    int bit_offset = index % 8;
    if(val)
        this->grid[byte_num] |= (1 << bit_offset);
    else
        this->grid[byte_num] &= ~(1 << bit_offset);
}

