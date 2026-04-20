---
name: bug-analysis
description: |
  Analyze bug reports for SDK issues. Auto-detects SDK type from log files (IDK3, IDK4, IDK5, ICS) and platforms (iOS, Android, HarmonyOS). Clones repositories, checks out commits, and identifies root causes.
---

# Bug Analysis

Systematic process for analyzing bugs using log files and SDK source code.

---

## SDK Family Overview

| SDK Family | Platforms | Description |
|------------|-----------|-------------|
| **IDK3** | iOS, Android | Ingeek Digital Key SDK v3.x |
| **IDK4** | iOS, Android | Ingeek Digital Key SDK v4.x |
| **IDK5** | iOS, Android | Ingeek Digital Key SDK v5.x |
| **ICS** | iOS, Android, HarmonyOS | Intelligent Car Connection SDK |

**HarmonyOS Special Rule**: Only ONE SDK exists for HarmonyOS - **ICS**. No IDK3/IDK4 distinction for HarmonyOS.

**IDK5 Android Submodule Architecture**: IDK5 Android includes ICS Android SDK as a submodule at `submodule/ics-sdk`. When analyzing IDK5 Android bugs, also check the ICS Android submodule for root cause.

---

## Phase 1: SDK Detection from Log File

### 1.1 Log Format Identification Matrix

| SDK | Platform | Log Pattern | Version | commitId |
|-----|----------|-------------|---------|----------|
| **IDK3** | iOS | `💛[N]`, `💙[D]`, `💔[E]`, `💜[W]` + `[MM-DD HH:MM:SS:ms]` | `3.x.x` | ✅ 8-char |
| **IDK3** | Android | `D/`, `I/`, `E/`, `V/` + obfuscated names + `YYYY-MM-DD` (dashes) | `3.x.x` | ❌ |
| **IDK4** | iOS | `🔓🛠️💚[T]`, `🔓🛠️💙[D]` + `DFM-X.XX.X` + `YYYY-MM-DD` | `4.x.x` | ✅ 8-char |
| **IDK4** | Android | `I/🛠[DEBUG]`, `E/🛠[DEBUG]` + `YYYY-MM-DD` (dashes) | `4.x.x` | ❌ |
| **IDK5** | Android | `D:`, `E:`, `I:`, `V:` (colon) + `VENDOR_` prefix + vendor name (GWM/Voyah/Bestune/GAC) | `3.x.x` | ❌ |
| **ICS** | iOS | `💙[D]`, `💚[I]`, `🧡[W]`, `💔[E]` + `spec/cot3/cot3.cpp` | `v3.x.x.x-build` | ❌ |
| **ICS** | Android | `D:`, `E:`, `I:`, `V:` (colon) + `spec/cot3/cot3.cpp` | `5.x.x` | ❌ |
| **ICS** | HarmonyOS | `💛[I]`, `💙[D]`, `💔[E]` + `YYYY/MM/DD` (slashes) + `0000:` line prefix | `4.x.x`/`5.x.x` | ❌ |

### 1.2 Detailed Recognition Rules

#### IDK3 iOS
```
[03-25 14:11:00:901]-💛[N]: -[IngeekSecureKeyKit disconnectVehicle:] [910] Disconnect vehicle
[03-25 14:11:01:240]-💛[N]: -[IngeekSecureKeyKit initSecureKeyWithConfiguration:] [289] SDK version: 3.0.10, commitId: aed791a7
```
- Timestamp: `[MM-DD HH:MM:SS:ms]` (month-day, no year)
- Log levels: `💛[N]` Normal, `💙[D]` Debug, `💔[E]` Error, `💜[W]` Warning
- Module prefix: `IngeekSecureKeyKit`, `IngeekDigitalKeyKit`, `VCK*`
- Version: `3.x.x`
- commitId: 8-character hex (e.g., `aed791a7`)

#### IDK3 Android
```
2026-03-27 12:02:12:873 D/O000000o init() start...,sdkVersionName:3.2.5,sdkVersionCode:3205
2026-03-27 12:02:13:637 D/IngeekServerVersion onSuccess{}
2026-03-27 12:02:19:200 E/CommonJsonCallback 网络请求时发生异常，errorCode = 2017
```
- Timestamp: `YYYY-MM-DD HH:MM:SS:ms` (dashes!)
- Log levels: `D/` DEBUG, `I/` INFO, `E/` ERROR, `V/` VERBOSE (standard Android)
- Module names: Obfuscated (`O000000o`, `O0000o0`) or `Ingeek*`
- Version: `3.x.x`
- Error codes: `2017` (钥匙不存在), `3003` (连接失败)

#### IDK4 iOS
```
7751: [2026-03-26 16:12:04.347]-[(26.1) (iPhone17,2)]-🔓🛠️💚[T]: -[IngeekBleIcce parseIcceData:] [1472] Ble icce parse data
💛[N]: -[IngeekDigitalKeyKit initSDK] [289] SDK version: 4.15.3, commitId: e8e6ac7a, release date: 20260327-14:30
```
- Line number prefix: `7751:`
- Timestamp: `YYYY-MM-DD HH:MM:SS.mmm`
- Component info: `(iOS Version) (iPhone Model)`
- Log levels: `🔓🛠️💚[T]` Trace, `🔓🛠️💙[D]` Debug
- DFM version: `DFM-4.13.6 (0c10b09)`
- commitId: 8-character hex (e.g., `e8e6ac7a`)

#### IDK4 Android
```
2026-03-27 11:06:09:340 I/🛠[DEBUG]LoggerManager: enter logger manager init, thread-pool-0
2026-03-27 11:06:09:350 E/🛠[DEBUG]INIT_SdkInitialize: 当前 SDK 为 debug 版本
2026-03-27 11:06:27:402 E/🛠[DEBUG]BleOperator: enter onConnectFailure, errorCode: 121000
```
- Timestamp: `YYYY-MM-DD HH:MM:SS:ms` (dashes!)
- Log levels: `I/🛠[DEBUG]`, `D/🛠[DEBUG]`, `E/🛠[DEBUG]`
- Module names: Clear names (`LoggerManager`, `BleOperator`, `LegacyKeyManager`)
- Version: `4.x.x`
- Error codes: `121000` (GATT timeout), `100201` (operation timeout)

#### IDK5 Android
```
2026-03-27 11:06:09:340 I: [VENDOR_VendorManager] Vendor init start
2026-03-27 11:06:09:350 E: [VENDOR_VendorManager] Vendor key not found
2026-03-27 11:06:27:402 D: [VENDOR_VendorKeyFactory] Key factory created
```
- Timestamp: `YYYY-MM-DD HH:MM:SS:ms` (dashes!)
- Log levels: `D:`, `I:`, `E:`, `V:` (colon, same as ICS Android)
- Module prefix: `VENDOR_` + vendor name (GWM, Voyah, Bestune, GAC)
- Version: `3.x.x`
- Vendors: GWM, Voyah, Bestune, GAC
- **Note**: Uses ICS Android as submodule, check both layers for bugs

#### ICS iOS
```
[2026-03-26 18:21:30.506]-💙[DEBUG]: -[ICSKeyFactory _setup] [365] [DK] ICSCarKey core version v3.1.3.2-31756
💙[DEBUG]: COT3 [getDigitalKey] get digital key: 623835 ( spec/cot3/cot3.cpp [607] )
💔[ERROR]: SPEC [getDigitalKeyInternal] no digital key for: 623835 ( spec/common/spec_base.cpp [64] )
```
- Log levels: `💙[DEBUG]`, `💚[INFO]`, `🧡[WARN]`, `💔[ERROR]`
- Version: `v3.x.x.x-build` (e.g., `v3.1.3.2-31756`)
- C++ stack traces: `spec/cot3/cot3.cpp`, `spec/common/spec_base.cpp`
- Module prefix: `ICS*` (`ICSKeyFactory`, `ICSCarKeyImpl`)

#### ICS Android
```
2026-03-26 14:17:46.019 E: [CrashCheck] Crash Version 2
2026-03-26 14:18:07.345 E: [ICSCarKeyImpl] ICSCarKeyImpl create, hash = 175351462
2026-03-26 14:23:50.911 D: [ICSCarKeyImpl] COT3 [processData] process data, keyidx: 8606BD
```
- Log levels: `D:`, `I:`, `E:`, `V:` (colon, not slash!)
- Version: `5.x.x` (e.g., `5.9.0 build 48506`)
- C++ references: `spec/cot3/cot3.cpp` via JNI
- Module prefix: `ICS*`, `SecurityEngineImpl`

#### ICS HarmonyOS
```
0000: 2026/03/25 16:16:55:58 💛[I]: [API-CONFIG] setUrl: https://dk.dfmc.com.cn:33102
0006: 2026/03/25 16:16:55:67 💛[I]: [Voyah CarKey] Voyah CarKey Version: 5.2.2
0052: 2026/03/25 16:37:12:727 💛[I]: [CarKey] SDKCore [printVersionInfo] cot2 enabled
```
- Line number prefix: `0000:`, `0001:`, etc.
- Timestamp: `YYYY/MM/DD HH:MM:SS:ms` (slashes!)
- Log levels: `💛[I]`, `💙[D]`, `💔[E]`
- Version: `4.x.x` or `5.x.x`
- HarmonyOS markers: `ohos.permission.*`, `EntryAbility`, `UIAbilityContext`

### 1.3 commitId Extraction Pattern

**For IDK3 iOS and IDK4 iOS only:**

```regex
SDK version: \d+\.\d+\.\d+, commitId: ([a-f0-9]{8})
```

**Extraction command:**
```bash
grep -oE "commitId: [a-f0-9]{8}" logfile.txt | head -1 | cut -d' ' -f2
```

**Example:**
```
Input:  💛[N]: -[IngeekDigitalKeyKit initSDK] [289] SDK version: 4.15.3, commitId: e8e6ac7a, release date: 20260327-14:30
Output: e8e6ac7a
```

### 1.4 Quick Detection Flowchart

```
Check log format:
├── Has emoji 💛💙💔💜?
│   ├── Timestamp with [MM-DD]? → IDK3 iOS
│   ├── Timestamp with YYYY/MM/DD (slashes)? → ICS HarmonyOS
│   └── Has 🔓🛠️? → IDK4 iOS
├── Has 🛠[DEBUG]?
│   └── I/🛠[DEBUG], E/🛠[DEBUG] → IDK4 Android
├── Has D/, I/, E/, V/ (standard Android)?
│   ├── Obfuscated modules (O000000o) + version 3.x → IDK3 Android
│   └── Clear modules + version 3.x → IDK3 Android
├── Has D:, I:, E: (colon)?
│   ├── Has VENDOR_ prefix? → IDK5 Android
│   └── spec/cot3/cot3.cpp → ICS Android
└── Has spec/cot3/cot3.cpp with emoji?
    └── ICS iOS
```

---

## Phase 2: Repository Setup

### 2.1 SDK to Git Repo Mapping

| SDK | Platform | Git Repository | Default Branch |
|-----|----------|----------------|----------------|
| **IDK3** | iOS | `git@gitlab.ingeek.com:qz/mobile/ios/idk_mob_sdk2_ios.git` | `master` |
| **IDK4** | iOS | `git@gitlab.ingeek.com:qz/mobile/ios/idk-mob-sdk-ios.git` | `main` |
| **IDK5** | iOS | `git@gitlab.ingeek.com:qz/mobile/ios/idk_mob_sdk5_ios.git` | `main` |
| **ICS** | iOS | `git@gitlab.ingeek.com:hz/mobile/ics-ios-sdk.git` | `main` |
| **IDK3** | Android | `git@gitlab.ingeek.com:qz/mobile/android/idk_mob_sdk_android.git` | `master` |
| **IDK4** | Android | `git@gitlab.ingeek.com:qz/mobile/android/idk-mob-sdk-4-android.git` | `main` |
| **IDK5** | Android | `git@gitlab.ingeek.com:qz/mobile/android/idk-mob-sdk5-android.git` | `main` |
| **ICS** | Android | `git@gitlab.ingeek.com:hz/mobile/ics-android-sdk.git` | `main` |
| **ICS** | HarmonyOS | `git@gitlab.ingeek.com:ics/harmony/carkey.git` | `main` |

### 2.2 Workspace Path

Clone SDK repositories to Qoder workspace for analysis:

```
~/.qoder/workspace/sdk-repos/{sdk-name}/
```

**Example:**
```
~/.qoder/workspace/sdk-repos/ics-harmony-sdk/
~/.qoder/workspace/sdk-repos/idk-mob-sdk-ios/
~/.qoder/workspace/sdk-repos/idk_mob_sdk_android/
```

### 2.3 Clone Repository (if needed)

```bash
# Create workspace if not exists
mkdir -p ~/.qoder/workspace/sdk-repos

# Clone to workspace
git clone <repository-url> ~/.qoder/workspace/sdk-repos/{sdk-name}

# Example for IDK3 Android:
git clone git@gitlab.ingeek.com:qz/mobile/android/idk_mob_sdk_android.git \
    ~/.qoder/workspace/sdk-repos/idk_mob_sdk_android

# Example for ICS HarmonyOS:
git clone git@gitlab.ingeek.com:ics/harmony/carkey.git \
    ~/.qoder/workspace/sdk-repos/ics-harmony-sdk
```

### 2.4 Checkout Specific Commit (Priority Order)

**CRITICAL**: Always checkout the exact commit from the log file.

**Priority order:**
1. **Priority 1: commitId from log** → `git checkout <8-char-commitId>` (most precise!)
2. **Priority 2: User specified branch** → `git checkout {branch}`
3. **Priority 3: Default branch** → Use SDK default (main/master)

```bash
cd <repository-path>

# Verify current state
git log -1 --oneline

# Fetch if needed
git fetch --all

# Checkout specific commit
git checkout <commit-hash>

# Verify checkout
git log -1 --oneline
```

---

## Phase 3: Source Code Analysis

### 3.1 Source Code Directory Mapping

| SDK | Platform | Version | Source Directory | Key Modules |
|-----|----------|---------|-----------------|-------------|
| **IDK3** | iOS | `2.x`/`3.x` | `code/Components/` | `IngeekSecureKeyKit.m`, `IngeekDigitalKeyKit.m` |
| **IDK4** | iOS | `4.x` | `code/Components/` | `IngeekBleIcce.m`, `VCKBleManager.m` |
| **IDK5** | iOS | `5.x` | `code/Components/` | `IngeekBleIcce.m`, `VCKBleManager.m` |
| **IDK3** | Android | `3.x.x` | `app/src/main/` | `IngeekDigitalKeyKit`, `IngeekSecureKeyKit` |
| **IDK4** | Android | `4.x.x` | `app/src/main/` | `BleOperator`, `LegacyKeyManager` |
| **IDK5** | Android | `3.x.x` | `lib_sdk/src/{vendor}/java/` | `VendorManager`, `VendorCarKey`, `VendorKeyFactory` |
| **ICS** | iOS | `v3.x.x.x-build` | `code/Components/`, `cmake/se/` | `ICSCarKeyImpl.swift`, `cot3.cpp` |
| **ICS** | Android | `5.x.x` | `app/src/main/` | `ICSCarKeyImpl`, `SecurityEngineImpl` |
| **ICS** | HarmonyOS | `4.x.x`/`5.x.x` | `src/main/ets/` | `CarKeyCapability.ts`, `WalletManager` |

**IDK5 Android Vendor Paths**: `lib_sdk/src/{gwm|voyah|bestune|gac}/java/com/ingeek/{vendor}/`

### 3.2 Common Error Codes

#### IDK3 Error Codes

| Code | Meaning | Source Location |
|------|---------|----------------|
| `2017` | 钥匙不存在 (Key not found) | `IngeekDigitalKeyKit` |
| `3001` | Connect vehicle failed | `IngeekSecureKeyKit` |
| `3003` | Connection failed (wrapper) | `VehicleConnectHelper` |

#### IDK4 Error Codes

| Code | Meaning | Source Location |
|------|---------|----------------|
| `121000` | GATT connection timeout | `VCKBleManager` |
| `100201` | Operation timeout | `VCKHttpClient` |
| `100100` | Bluetooth state error | `VCKBleManager` |
| `100101` | Bluetooth not enabled | `VCKBleManager` |
| `100102` | Bluetooth not authorized | `VCKBleManager` |
| `100110` | Bluetooth connection failed | `VCKBleManager` |
| `100107` | Bluetooth scan timeout | `VCKBleManager` |

#### ICS Error Codes

| Code | Meaning | Source Location |
|------|---------|----------------|
| `6000` | CCC get key failed | `ICSCCCCarKeyImpl` |
| `4052` | Connection error | `ICSCOT3V3CarKeyImpl` |
| `160006` | Wallet query failed | `CarKeyCapability.ts` |
| `1010200006` | Huawei Wallet error | `WalletManager` |

### 3.3 Locate Error Code in Source

```bash
# Search by error code
grep -r "2017\|3001\|121000" --include="*.ts" --include="*.swift" --include="*.kt" --include="*.java" --include="*.m" <repo-path>

# Search by method name
grep -r "supportsWearDevice\|isSupportWallet\|connectVehicle" --include="*.ts" <repo-path>

# Search by class/module
find <repo-path> -name "*CarKey*" -o -name "*BleManager*"
```

### 3.4 Data Flow Tracing (MANDATORY - DO THIS FIRST)

**This is the most critical step. Always trace the data flow from input to crash before forming any root cause hypothesis.**

The most common mistake in crash analysis is to start from the crash point (e.g., `abort()`, `assert()`) and work backwards to invent a plausible explanation. This leads to wrong root causes. Instead, start from the actual input data and trace forward through every transformation until the crash.

#### 3.4.1 The Data-First Principle

```
WRONG approach (crash-first):
  crash → abort() → assert(false) → ??? sessionKeySize must be wrong → invent explanation

RIGHT approach (data-first):
  raw input → parse/transform → intermediate data → next transform → ... → crash
```

#### 3.4.2 Step-by-step Data Flow Tracing

1. **Identify the actual input data** from the log file (e.g., BLE bytes, API response, file content)
2. **Parse the input through each layer** - trace byte-by-byte through protocol parsing, data extraction, format conversion
3. **Compute the intermediate values** at each step - what does the data look like after each transformation?
4. **Validate the data at each step** - is the size correct? Is the alignment correct? Are values in expected ranges?
5. **Only then form a root cause hypothesis** based on where the data first went wrong

#### 3.4.3 Key Things to Trace in SDK Bug Analysis

For BLE-related crashes (most common in IDK SDKs):
- **Raw BLE notification bytes** → VCKBleNotifyData parsing → `notifyData.data` extraction → what bytes/length are passed to the next layer
- **Protocol header fields**: message ID, sequence number, data length - verify each field against constants
- **Packet reassembly**: single-packet vs multi-packet detection, `completed` flag logic
- **Data extraction**: header stripping, extra data removal, offset calculation - verify return values are used

For encryption/decryption crashes:
- **Input data length** to `decryptData()` - must be > 16 bytes (CMAC is 16 bytes)
- **Session key validity** - `sessionKeySize` must be 16 or 32
- **Block alignment** - AES-CBC requires data length to be a multiple of 16

#### 3.4.4 Common Data Flow Bugs

| Bug Pattern | Example | Detection Method |
|-------------|---------|-----------------|
| **Partial data treated as complete** | BLE notification fragment processed before reassembly | Check `completed` flag logic against actual packet sequence |
| **Return value not stored** | `location = [self parseReply:... location:]` → `location` not updated | Grep for method calls where return value is discarded |
| **Type truncation** | `uint16_t` → `uint8_t` implicit conversion loses data | Check struct field types vs assigned values |
| **Signed/unsigned mismatch** | `dataCount - 16` when `dataCount < 16` wraps to huge number | Check for subtraction that can go negative then implicit cast to unsigned |
| **Wrong offset calculation** | Header length hardcoded vs dynamically computed | Trace offset values step by step with actual data |

### 3.5 Trace Execution Flow

1. **Entry point** - Where the failed method is called
2. **Processing** - What transformations occur
3. **External calls** - APIs, SDKs, system services
4. **Error handling** - How errors are caught and propagated

### 3.6 Identify Cache Mechanisms

```
Look for:
- Cache keys and storage locations
- Cache invalidation logic
- Cached values for error conditions
- Difference between SDK cache and app-layer cache
```

---

## Phase 4: Root Cause Analysis

### 4.1 Data-First Root Cause Identification

**Before classifying the error source, verify your hypothesis against the actual data.**

#### 4.1.1 Hypothesis Validation Checklist

Before concluding a root cause, answer these questions:

1. **Does the data support it?** - Can you show the specific bytes/values that lead to the crash?
2. **Is the data path complete?** - Have you traced from the original input to the crash point through every transformation?
3. **Are there alternative explanations?** - What other conditions could produce the same crash?
4. **Can you disprove your hypothesis?** - What data would prove your theory wrong?

#### 4.1.2 Common Wrong Hypothesis Patterns

| Wrong Pattern | What Happens | Right Approach |
|---------------|--------------|----------------|
| **Assert-first** | See `assert(false)` → assume the assertion condition is violated | Trace what data reaches the assert - is the function even called with valid input? |
| **Stack-only** | Read crash stack → explain each frame → conclude from frame names | Stack tells you WHERE, not WHY. Trace the data that flows through those frames. |
| **Symbolication artifact** | Trust symbolicated symbol names literally (e.g., `setVin:`) | Verify offset distances between frames - nearby symbols can be wrong |
| **Single-cause assumption** | Find one bug and stop | Many crashes have multiple contributing bugs (e.g., data parsing bug + missing length validation) |

### 4.2 Determine Error Source

| Source | Indicators |
|--------|------------|
| **External Service** | Error codes from APIs, SDKs, system services |
| **SDK Logic** | Error handling gaps, missing fallbacks, data parsing bugs |
| **App Layer** | Wrapper code issues, incorrect caching |
| **Configuration** | Missing setup, wrong parameters |

### 4.3 Identify the Fix Location

```
Layer hierarchy:
1. External Service (Huawei Wallet, etc.) - may need support ticket
2. SDK Core - requires SDK update
3. SDK Wrapper/OEM Layer - requires OEM app update
4. App Integration - requires app code fix
```

When multiple bugs contribute to a crash, fix ALL of them:
- **Root trigger** (the bug that produces bad data) - e.g., protocol parsing error
- **Crash cause** (the bug that turns bad data into a crash) - e.g., missing length validation
- Both must be fixed: the trigger to prevent bad data, and the crash cause to make the SDK resilient

### 4.4 Document Root Cause

```
Root Cause:
- [Data Flow] Input <X> is parsed/transformed by <method> which produces <bad value>
- [Trigger] <method> has bug <description> causing <bad value> when <condition>
- [Crash] <bad value> flows to <crash_method> which lacks validation for <condition>
- [Result] <crash_method> crashes with <signal>

Example:
- [Data Flow] BLE notification 90A1... (20 bytes) is parsed by VCKBleNotifyData
- [Trigger] parseData: does not store return value from parseReplySerialNumberAndMessageIdAndResult,
  causing notifyData.data to extract wrong 8 bytes instead of correct 32 bytes
- [Crash] decryptData receives dataCount=8, computes inputData(8-16) which wraps to huge size_t
- [Result] std::bad_alloc → std::terminate() → abort() → SIGABRT
```

---

## Phase 5: Fix Recommendations

### 5.1 Propose Solutions

For each viable fix option, provide:
1. **Location** - Exact file and method
2. **Change** - What code to add/modify
3. **Impact** - Side effects and considerations
4. **Priority** - Recommended vs alternative

### 5.2 Code Examples

```typescript
// Before (problematic code)
async function problematicMethod() {
  try {
    return await externalService.call()
  } catch (error) {
    return Promise.reject(error)  // Error propagates unhandled
  }
}

// After (fixed code)
async function fixedMethod() {
  try {
    return await externalService.call()
  } catch (error) {
    if (error.code === SPECIFIC_ERROR_CODE) {
      // Handle specific error
      await initializeEnvironment()
      return await externalService.call()  // Retry
    }
    return Promise.reject(error)
  }
}
```

### 5.3 Prevention Measures

- Add error handling for specific error codes
- Implement cache invalidation on state changes
- Add retry logic for transient errors
- Improve logging for debugging

---

## Network Endpoints Reference

| SDK | Environment | URL |
|-----|-------------|-----|
| **IDK3 iOS** | Production | `https://www.gacne.com.cn/newv1/lifemain/icv/bluetooth-api/ingeek-vck-gateway/ingeek.vck.service/apis/v3/ingeek/business_operation` |
| **IDK4 iOS** | UAT | `https://uat-jmcgf-idp.ingeek.com` |
| **IDK4 iOS** | Production | `https://dk.dfmc.com.cn:33102` |
| **ICS** | UAT | `https://vos5-integration.dk-car.com` |
| **ICS** | Production | `https://dk.dfmc.com.cn:33102` |
| **ICS** | Tracking | `https://diting-collector.ingeek.com/diting-collector-server-srv` |

---

## Bug Analysis Checklist

```
📋 Bug Analysis Progress:

Phase 1: Log Analysis
- [ ] 1. SDK type detected (IDK3/IDK4/ICS + platform)
- [ ] 2. Error codes extracted
- [ ] 3. Timeline built
- [ ] 4. commitId extracted (if available)

Phase 2: Repository Setup
- [ ] 5. Repository located
- [ ] 6. Repository cloned (if needed)
- [ ] 7. Correct commit/branch checked out

Phase 3: Code Analysis
- [ ] 8. Error code found in source
- [ ] 9. DATA FLOW TRACED from input to crash (MANDATORY - do this BEFORE forming hypothesis)
- [ ] 10. Execution flow traced
- [ ] 11. Cache mechanisms identified

Phase 4: Root Cause
- [ ] 12. Hypothesis validated against actual data
- [ ] 13. Error source classified
- [ ] 14. Fix location determined (both trigger and crash cause)
- [ ] 15. Root cause documented with data flow evidence

Phase 5: Solution
- [ ] 16. Solutions proposed
- [ ] 17. Code examples provided
```

---

## Tips

1. **Always checkout the exact commit** - Code may differ significantly between versions
2. **Check both SDK and wrapper layers** - The bug may not be in the SDK
3. **Don't assume caching behavior** - Verify where caching occurs
4. **Map error codes** - External error codes often map to internal codes
5. **Check error handling** - Many bugs are due to unhandled specific error codes
6. **HarmonyOS = ICS only** - No IDK3/IDK4 for HarmonyOS platform
7. **IDK3 vs IDK4 Android** - Completely different log formats!
8. **Timestamp formats matter** - Dashes vs slashes, with/without year
9. **IDK5 Android uses ICS submodule** - Check `submodule/ics-sdk` for ICS-level bugs
10. **ALWAYS trace data flow first** - Never start root cause analysis from the crash point. Start from the actual input data and trace forward through every transformation. The crash is the symptom; the data transformation bug is the disease.
11. **Validate symbolicated stack frames** - Symbolicated names can be wrong (nearest symbol, not exact). Check offset distances between frames to verify symbol accuracy.
12. **Multiple bugs often coexist** - A crash usually involves both a trigger (produces bad data) and a missing defense (fails to handle bad data). Fix both.

---

## Unknown Log Format Handling

If log format doesn't match any known pattern:

1. **Conservative Analysis (Immediate)**
   - Extract all error codes and messages
   - Build chronological timeline
   - Analyze error frequency
   - Provide generic troubleshooting

2. **Ask User for Context**
   ```
   "这份日志的格式我不认识，请告诉我：
   1. 这是什么 SDK？(IDK3 / IDK4 / ICS)
   2. 哪个平台？(iOS / Android / HarmonyOS)
   3. 仓库地址是什么？
   4. 是否有 commitId 或分支名？"
   ```

3. **Continue with Manual Input**
   - Clone the specified repository
   - Switch to the correct branch/commit
   - Search for error codes in source

4. **Update Skill** - Add new log format pattern to skill documentation
