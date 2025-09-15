#!/bin/bash
set -e
echo "Running inside container: $1 + $2"
cd "$GITHUB_WORKSPACE"

compiler=$2
if [[ $compiler == gcc-* ]]; then
  export CC=$compiler
  export CXX=g++-${compiler#gcc-}
elif [[ $compiler == clang-* ]]; then
  export CC=$compiler
  export CXX=clang++-${compiler#clang-}
fi

cmake -B build -DCMAKE_CXX_COMPILER=$CXX
cmake --build build -- -j$(nproc)
ls build/*
./build/runner_test
