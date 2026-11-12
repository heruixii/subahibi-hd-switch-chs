# 第六十七轮：原PC BGI虚拟机执行核心第一阶段——安全结构、合成运算与真实130场景跳转表

日期：2026-10-19
项目根目录：D:/switch游戏/素晴日/素晴日整合/1.游戏合集/移植新版素晴日ns

## 本轮实际新增工程

P268已完成130段合法原PC BurikoCompiledScriptVer1.00场景的C99结构读取；本轮新增独立ISO C99原字节码安全前端及仅限自造合成测试使用的小型执行核心。不触及游戏原文件、已安装NS游戏与玩家Save。

目录：03_脚本工作区/P270_原BGI_VM首批堆栈跳转C99隔离执行核_未证明真实引擎语义/

- p270_bgi_vm_core.h：VM指令表、1024值运算栈、最多1000000条指令等硬限制。
- p270_bgi_vm_core.c：对原scene做magic/header/32bit小端opcode/参数/CP932 NUL字符串/ret检查、偏移索引与所有push_offset目标边界验证。只有明确synthetic_only=1才执行自造的运算测试；真实原BGI永远在第一条指令前返回NEEDS_SEMANTICS。
- p270_synthetic_vm_test.c：47项C99合成测试断言，涉及add/sub/mul/div/mod/eq/bool_zero、合成jmp/jc条件分支、异常opcode/头/字符串/RET/目标、除零/溢出/栈下溢/循环指令预算与外部BGI API拒绝。
- p270_original_BGI_opcode_C99_frontend_host_cli.c：读取真正原130个编译剧本的只读CLI，报告指令数/ret/合法CFG目标，真实VM执行计数为0。

实际PC源原样比对：130/130场景SHA验证，743326条opcode与原独立Python反汇编严格对应，原523个push_offset目标全部落在真实指令起始偏移，没有跳入字符串数据/操作数中间。使用本地可信GCC编译真正源码，又以官方SHA锁定的Zig将真实C99 VM核心编译为ARM64 ELF64 ET_REL，而非伪造NRO或运行历史第三方Windows可执行工具。

## 重要限制

当前的合成分支约定并未被确认就是BGI原始VM语义。实际原BGI load_base/store_base栈帧、jc条件、jmp/call/ret调用、注册引擎函数与参数规则、中文对白/选项/CG/Save都需要单独证据才能逐渐启用。真实源的VM指令实际执行=0，不能宣称已能运行一章剧情。本轮ARM64成果仅源库对象，未嵌入已有高清与音频QA NRO，也没有Nintendo Switch hbmenu/GPU/DAC/存档实测。

验收脚本：01_工具脚本/verify_p270_BGI_C99_VM_safe_synthetic_stack_jump_and_130_original_CFG_offsets.py
报告：06_测试记录/P83_真正C99_BGIVM合成堆栈算术条件跳转47断言与130源场景523跳转边界_真AARCH64对象未执行原剧本.json
全量门禁：06_测试记录/P84_第六十七轮_BGI_VM安全堆栈与523有效跳转原场景全边界_313工具总门禁.log

正式状态：BLOCKED_NOT_SAFE_TO_INSTALL。


## P271：真实BGI执行缺口的原指令频率优先级审计

为确保下一阶段真正实现栈帧/变量/条件跳转时不凭猜测，本轮逐源SHA复核130个真实PC场景，读取共743326条原BGI字节码的真实编码指令ID。其间实际出现161种opcode，原push_offset共523次且目标全部边界合法。原条件跳转jc共186条，直接编码参数全部为0；但该字节值的真假/跳转约定尚未证实，不能自动采用本轮自造VM对jc的假设。无条件jmp共207条，原BGI场景中call(0x01a)为0条。每个场景均可见load_base与store_base（各共260次）；push_base_offset共3135次，load(0x008)共716次、move(0x009)共1615次、异常注册和解除各130次。因此下阶段顺序为：依据原引擎/BP证明base frame/slot布局和异常处理，再证明条件变量比较与跳转实际取值、系统/文本/图层方法及音画时钟，最后结合真实中文文本分支执行。当前原场景指令真实执行=0。

新增单独来源审计：01_工具脚本/verify_p271_original_BGI_VM_opcodes_priority_semantics_distribution_readonly.py
报告：06_测试记录/P85_原130BGI场景743326条opcode执行语义缺口_条件jc实参统计和VM先后依赖_不执行原游戏.json

该报告也加入中央门禁：必须在全量130原剧本和所有SHA的基础上确认161种原opcode、186个jc(0)源编码及base frame前置依赖，才能允许继续。所有数据仍为静态代码流证据，绝不能称NS已经运行原剧情。


## 完整总回归完成：314项工具PASS

在中央门禁里再次执行并确认：314工具全通过、91源SHA、4324旧QA文件、1505原高清PNG、33454原OGG安全原码流；P270真实130场景743326 opcode/523跳转目标、47项自造合成VM断言/5类外部API阻断、真正ARM64 C99目标对象，以及P271原161种opcode/jc(0)186次/260次原栈帧指令静态优先级，均通过。前轮P261真ARM64高清和原OGG诊断NRO的SHA未改变。\n\n不可变快照：06_测试记录/2026-10-19_第六十七轮_真实BGI130脚本523跳转161操作码合成安全47断言_314工具总快照.json\n\n所有真实原BGI剧情字节码实际执行仍为0，未在Switch真机运行；VM条件跳转、栈帧、原中文剧情、CG和完整音画同步均未完成。当前候选不能发布或直接安装，BLOCKED_NOT_SAFE_TO_INSTALL。\n