# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/znfs/project_ws/baxter/src/speech

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/znfs/project_ws/baxter/src/speech/src

# Utility rule file for speech_genlisp.

# Include the progress variables for this target.
include CMakeFiles/speech_genlisp.dir/progress.make

speech_genlisp: CMakeFiles/speech_genlisp.dir/build.make

.PHONY : speech_genlisp

# Rule to build all files generated by this target.
CMakeFiles/speech_genlisp.dir/build: speech_genlisp

.PHONY : CMakeFiles/speech_genlisp.dir/build

CMakeFiles/speech_genlisp.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/speech_genlisp.dir/cmake_clean.cmake
.PHONY : CMakeFiles/speech_genlisp.dir/clean

CMakeFiles/speech_genlisp.dir/depend:
	cd /home/znfs/project_ws/baxter/src/speech/src && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/znfs/project_ws/baxter/src/speech /home/znfs/project_ws/baxter/src/speech /home/znfs/project_ws/baxter/src/speech/src /home/znfs/project_ws/baxter/src/speech/src /home/znfs/project_ws/baxter/src/speech/src/CMakeFiles/speech_genlisp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/speech_genlisp.dir/depend

