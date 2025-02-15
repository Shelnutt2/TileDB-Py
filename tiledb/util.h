#ifndef TILEDB_PY_UTIL_H
#define TILEDB_PY_UTIL_H

const uint64_t DEFAULT_INIT_BUFFER_BYTES = 1310720 * 8;
const uint64_t DEFAULT_EXP_ALLOC_MAX_BYTES = uint64_t(4 * pow(2, 30));

#define TPY_ERROR_STR(m)                                                       \
  [](auto m) -> std::string {                                     \
      return std::string(m) + " (" + __FILE__ + ":" +               \
             std::to_string(__LINE__) + ")");                                  \
  }();

#define TPY_ERROR_LOC(m)                                                       \
  throw TileDBPyError(std::string(m) + " (" + __FILE__ + ":" +                 \
                      std::to_string(__LINE__) + ")");

class TileDBPyError : std::runtime_error {
public:
  explicit TileDBPyError(const char *m) : std::runtime_error(m) {}
  explicit TileDBPyError(std::string m) : std::runtime_error(m.c_str()) {}

public:
  virtual const char *what() const noexcept override {
    return std::runtime_error::what();
  }
};

#endif // TILEDB_PY_UTIL_H
