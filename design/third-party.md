---
title: "Third Party"
description: "Third-Party Components in FalkorDB"
parent: "The FalkorDB Design"
nav_order: 4
redirect_from:
  - /third-party.html
  - /third-party
---

# Third-Party Components in FalkorDB

FalkorDB uses several third-party libraries to enhance its functionality. 

Below is a list of these libraries along with their respective licenses.

---

## Included Libraries

### 1. [GraphBLAS](https://github.com/FalkorDB/FalkorDB/blob/master/deps/GraphBLAS/LICENSE)
- **License**: [Apache License 2.0](https://github.com/FalkorDB/FalkorDB/blob/master/deps/GraphBLAS/LICENSE)

### 2. [xxHash](https://github.com/Cyan4973/xxHash/blob/bbb27a5efb85b92a0486cf361a8635715a53f6ba/LICENSE)
- **License**: [BSD 2-Clause License](https://github.com/Cyan4973/xxHash/blob/bbb27a5efb85b92a0486cf361a8635715a53f6ba/LICENSE)

### 3. [utf8proc](https://github.com/JuliaStrings/utf8proc/blob/master/LICENSE.md)
- **License**: [MIT License](https://github.com/JuliaStrings/utf8proc/blob/master/LICENSE.md)

### 4. [rax](https://github.com/antirez/rax/blob/master/COPYING)
- **License**: [BSD 2-Clause License](https://github.com/antirez/rax/blob/master/COPYING)

### 5. [oniguruma](https://github.com/kkos/oniguruma/blob/master/COPYING)
- **License**: [BSD License](https://github.com/kkos/oniguruma/blob/master/COPYING)

### 6. [libcypher-parser](https://github.com/FalkorDB/FalkorDB/blob/master/deps/libcypher-parser/LICENSE)
- **License**: [Apache License 2.0](https://github.com/FalkorDB/FalkorDB/blob/master/deps/libcypher-parser/LICENSE)

### 7. [C Thread Pool (thpool)](https://github.com/Pithikos/C-Thread-Pool?tab=MIT-1-ov-file#readme)
- **License**: [MIT License](https://github.com/Pithikos/C-Thread-Pool?tab=MIT-1-ov-file#readme)

### 8. [sds](https://github.com/antirez/sds?tab=BSD-2-Clause-1-ov-file#readme)
- **License**: [BSD 2-Clause License](https://github.com/antirez/sds?tab=BSD-2-Clause-1-ov-file#readme)

### 9. [MT19937-64](https://github.com/FalkorDB/FalkorDB/blob/master/src/util/mt19937-64.h#L8)
- **License**: [MIT License](https://github.com/FalkorDB/FalkorDB/blob/master/src/util/mt19937-64.h#L8)

### 10. [CRoaring](https://github.com/RoaringBitmap/CRoaring?tab=License-1-ov-file#readme)
- **License**: [Apache License 2.0](https://github.com/RoaringBitmap/CRoaring?tab=License-1-ov-file#readme)

### 11. RedisGraph
- **License**: [RSALv2](https://redis.io/legal/rsalv2-agreement/) or [SSPLv1](https://redis.io/legal/server-side-public-license-sspl/) or [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)

### 12. Redis
- **License**: [RSALv2](https://redis.io/legal/rsalv2-agreement/) or [SSPLv1](https://redis.io/legal/server-side-public-license-sspl/) or [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)

### 13. RediSearch
- **License**: [RSALv2](https://redis.io/legal/rsalv2-agreement/) or [SSPLv1](https://redis.io/legal/server-side-public-license-sspl/) or [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.html)

---

Each of these libraries is crucial for FalkorDB's performance, scalability, and functionality. For further details, consult the respective license files linked above.

{% include faq_accordion.html
  title="Frequently Asked Questions"
  q1="What license types are used by FalkorDB's third-party dependencies?"
  a1="FalkorDB's dependencies use a mix of permissive open-source licenses: **Apache 2.0** (GraphBLAS, libcypher-parser, CRoaring), **MIT** (utf8proc, C Thread Pool, MT19937-64), and **BSD 2-Clause** (xxHash, rax, sds, oniguruma)."
  q2="What is GraphBLAS used for in FalkorDB?"
  a2="GraphBLAS provides the sparse matrix operations that power FalkorDB's graph traversal engine. It implements a standard API for linear algebra operations on sparse matrices, enabling efficient graph queries through matrix multiplication."
  q3="Does FalkorDB's use of these libraries affect my project's licensing?"
  a3="FalkorDB itself is licensed under **SSPLv1**. The third-party libraries have their own permissive licenses (Apache, MIT, BSD) which are compatible. Your obligations are governed by FalkorDB's SSPLv1 license terms, not by the individual dependency licenses."
  q4="What is the relationship between FalkorDB and RedisGraph?"
  a4="FalkorDB originated from the RedisGraph project. RedisGraph is listed as a dependency under RSALv2/SSPLv1/AGPLv3 licensing. FalkorDB builds upon and extends the original RedisGraph codebase."
%}
