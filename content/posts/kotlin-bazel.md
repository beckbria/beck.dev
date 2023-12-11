---
title: "Building Kotlin in a Bazel environment"
date: 2023-12-10T23:23:09-08:00
draft: false
tags: ["Programming", "Bazel", "Kotlin"]
---

# Kotlin on Bazel

I've worked on the [Advent of Code](https://adventofcode.com) problems in a variety of languages.
I prefer to have them in one consistent build environment, so I standardized on [Bazel](https://bazel.build). 
There are several guides online which attempt to explain this process, but when trying to set up a project
from scratch rather than modify an existing Java (or other) project I found that none of them seemed
to capture everything that was required. These are the steps which worked for me.

## Why bazel?

Bazel is a powerful cross-language tool to generate consistent veriable build artifacts from source.
It can be painful to set up initially, but once it's running it's straightforward to extend and add
new directories to. It is likely overkill for most projects, but as I've worked with it in the past
it is my preferred solution for multi-language builds.

# Final outcome

If you'd like to skip the explanation and see an example of a Kotlin bazel project, see 
[this commit](https://github.com/beckbria/advent-of-code/commit/a3be0c01d89edf2b4dd1eed0dcf0950a364565ea)
where I added a barebones Kotlin project to my Advent of Code Project

# Adding a Kotlin build rule

## Setting up the JRE

Kotlin requires a Java runtime. This is configured at the project level rather than in a BUILD file.
The [official way to do this](https://bazel.build/docs/bazel-and-java#config-source-code) is by specifying
a Java version in your `.bazelrc` file. I find that using a remote JRE is sufficient unless you have
specific reasons to use a local version.

```
# .bazelrc
build --java_language_version=11 --java_runtime_version=remotejdk_11
```

## Adding Kotlin to your workspace

The [bazelbuild Github page](https://github.com/bazelbuild/rules_kotlin?tab=readme-ov-file#workspace)
has instructions for how to add the Kotlin rules to your `WORKSPACE` and `BUILD` files.

In your `WORKSPACE` you will add something like the following (IMPORTANT: I recommend getting the 
latest version from the Github above)

```
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

rules_kotlin_version = "1.9.0"
rules_kotlin_sha = "5766f1e599acf551aa56f49dab9ab9108269b03c557496c54acaf41f98e2b8d6"
http_archive(
    name = "rules_kotlin",
    urls = ["https://github.com/bazelbuild/rules_kotlin/releases/download/v%s/rules_kotlin-v%s.tar.gz" % rules_kotlin_version],
    sha256 = rules_kotlin_sha,
)

load("@rules_kotlin//kotlin:repositories.bzl", "kotlin_repositories")
kotlin_repositories() # if you want the default. Otherwise see custom kotlinc distribution below

load("@rules_kotlin//kotlin:core.bzl", "kt_register_toolchains")
kt_register_toolchains() # to use the default toolchain, otherwise see toolchains below
```

## Build Rules

You should now be able to import and use the `kt_jvm_library` and `kt_jvm_binary` rules in your
build files in a manner identical to how you would use the [Java rules](https://bazel.build/reference/be/java)

```
load("@rules_kotlin//kotlin:jvm.bzl", "kt_jvm_binary")

kt_jvm_binary(
    name = "01",
    srcs = glob(["*.kt"]),
    main_class = "beckbria.aoc2023.day01.MainKt",
    data = ["input.txt"],
    deps = ["//2023/utils"],
    visibility = ["//visibility:public"],
)
```

## Naming

The `main_class` for a binary references the class which contains a `main` function to be invoked. The namespace segments
and class file name must begin with a lowercase letter. `beckbria.aoc2023.day01.MainKt` will match a file named `main.kt`
but not a file named `Main.kt`.
