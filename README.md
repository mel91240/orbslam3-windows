# ORB-SLAM3 Windows build notes

This repository contains a Windows-oriented ORB-SLAM3 setup that was successfully built with Visual Studio 2022 on one machine, but runtime execution has not been fully validated yet. The current state is **build confirmed, runtime not fully tested**.

## Current status

The following artifacts were built successfully on Windows:
- `Thirdparty/Pangolin/lib/Release/pangolin.lib`
- `build_orbslam/Release/ORB_SLAM3.lib`
- `build_orbslam/Release/ORB_SLAM3.dll` 

This repository includes local fixes applied to make the Windows build succeed, especially around Pangolin, Boost, and MSVC/CMake compatibility.

## Environment used

Build was performed on Windows with:
- Visual Studio 2022 / MSBuild
- CMake
- OpenCV from `C:\opencv\build\install\x64\vc17\lib`
- Boost 1.67.0 from `C:\local\boost_1_67_0`
- Eigen vendored in `Thirdparty/eigen` 


Important: paths are still partially hardcoded in `CMakeLists.txt`, so cloning this repository alone is **not** enough to guarantee a successful build on another machine without reproducing the same dependency layout.

## Main fixes applied

### Pangolin
- `MSVC_USE_STATIC_CRT` set to `OFF` to avoid `/MT` vs `/MD` conflicts on MSVC.
- External GLEW build kept enabled.
- The embedded GLEW CMake file had to be patched from:
  - `CMAKE_MINIMUM_REQUIRED(VERSION 2.6)`
  to:
  - `cmake_minimum_required(VERSION 3.5)`
- Pangolin test targets may still fail on Windows because of `pthread.lib`, but `pangolin.lib` itself was built successfully and was sufficient for ORB-SLAM3.

### Boost
- The project expects Boost 1.67.0 in `C:\local\boost_1_67_0`.
- The required serialization library is:
  - `C:\local\boost_1_67_0\lib64-msvc-14.1\libboost_serialization-vc141-mt-s-x64-1_67.lib`
- A Windows-specific fix was required to disable Boost auto-linking:
  - `BOOST_ALL_NO_LIB` 

### ORB-SLAM3
- ORB-SLAM3 was configured and linked successfully after the Boost fix above.
- Some paths in the root `CMakeLists.txt` are machine-specific and may need to be adapted on another computer.

## Dependencies expected

Before configuring the project, make sure the following are available:

| Dependency | Expected location |
|---|---|
| Boost 1.67.0 | `C:\local\boost_1_67_0` |
| OpenCV | `C:\opencv\build\install\x64\vc17\lib` |
| Eigen | `Thirdparty/eigen` |
| Pangolin | `Thirdparty/Pangolin` | 

## Build sequence used

### 1. Build Pangolin

Pangolin was configured from a dedicated build folder with external GLEW enabled and static CRT disabled.

Example:
```bat
cmake -G "Visual Studio 17 2022" -A x64 -T host=x64 ..\Thirdparty\Pangolin ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DMSVC_USE_STATIC_CRT=OFF ^
  -DBUILD_EXTERN_GLEW=ON ^
  -DBUILD_EXTERN_LIBJPEG=OFF ^
  -DBUILD_EXTERN_LIBPNG=OFF ^
  -DBUILD_TESTS=OFF ^
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5
```

### 2. Build ORB-SLAM3

ORB-SLAM3 was configured with OpenCV like this:

```bat
cmake -S . -B build_orbslam -G "Visual Studio 17 2022" -A x64 ^
  -DCMAKE_BUILD_TYPE=Release ^
  -DOpenCV_DIR=C:\opencv\build\install\x64\vc17\lib
```

Then built with:

```bat
cmake --build build_orbslam --config Release --target ORB_SLAM3
```

## Portability notes

This repository should currently be considered a **working build record**, not a fully portable Windows package. Another Windows machine may still require:
- matching Boost installation layout,
- matching OpenCV installation path,
- Visual Studio / MSVC compatibility,
- small path edits in `CMakeLists.txt`. 

## Next recommended step

The next useful step is to validate runtime execution with a real dataset and then replace hardcoded local paths with cleaner configuration variables or documented setup steps.

## Runtime validation with EuRoC MH01 (Monocular)

The Windows build has been successfully validated at runtime on the EuRoC MAV dataset using the monocular example and the `MH_01_easy` sequence. 

### Prerequisites

- The project must be built successfully as described above. 
- The EuRoC dataset must be downloaded in **ASL format** (image folders with `mav0`), not only as a ROS bag. 
- The vocabulary file `ORBvoc.txt` must be extracted from `ORBvoc.txt.tar.gz` into the `Vocabulary` folder. 

Example dataset layout outside the repository:

```text
C:\Users\melan\Datasets\EuRoC\MH01\
    mav0\
        cam0\
            data\
                1403636579763555584.png
                ...
```

Expected repository layout:

```text
orbslam3-windows\
    Vocabulary\
        ORBvoc.txt
        ORBvoc.txt.tar.gz
    Examples\
        Monocular\
            EuRoC.yaml
            EuRoC_TimeStamps\
                MH01.txt
            Release\
                mono_euroc.exe
```

### Command used on Windows

From the root of this repository:

```bat
Examples\Monocular\Release\mono_euroc.exe ^
  Vocabulary\ORBvoc.txt ^
  Examples\Monocular\EuRoC.yaml ^
  C:\Users\melan\Datasets\EuRoC\MH01 ^
  Examples\Monocular\EuRoC_TimeStamps\MH01.txt ^
  dataset-MH01_mono
```

This follows the same argument structure as the official EuRoC monocular example in ORB-SLAM3. 

If the setup is correct, the Pangolin viewer opens and the camera trajectory / map is visualized while processing the `MH01` sequence. 

### Common issues

- If `opencv_world4140.dll` is missing, copy the DLL from the local OpenCV `bin` folder next to `mono_euroc.exe`.
- If `Wrong path to vocabulary` appears, make sure `ORBvoc.txt` has been extracted and the first argument points to the real text file. 
- If `Failed to load image at ...\mav0\cam0\data\...png` appears, check that the dataset was fully downloaded and extracted, and that the path passed to the dataset points directly to the folder containing `mav0`. 