#SingleInstance
;基于火er作品修改
;久岐忍会导致错误
;---------------------------引用贴入------------------------------

;#Include genshin.ahk


class Config {

    static game_name_cn:='YuanShen.exe'
    static game_name_global:='GenshinImpact.exe'
}

class Genshin {
    static get_game_pos() {
        if ProcessExist(Config.game_name_cn) {
            WinGetClientPos(, , &width, &height, 'ahk_exe ' Config.game_name_cn)
        } else if ProcessExist(Config.game_name_global) {
            WinGetClientPos(, , &width, &height, 'ahk_exe ' Config.game_name_global)
        } else {
            width := 0
            height := 0
        }
        return [width, height]
    }

    static is_game_exist() {
        return ProcessExist(Config.game_name_cn) or ProcessExist(Config.game_name_global)
    }

    static is_game_active() {
        return WinActive('ahk_exe ' Config.game_name_cn) or WinActive('ahk_exe ' Config.game_name_global)
    }
}

class Point {
    __New(x := '', y := '') {
        this.x := x
        this.y := y
        this.x0 := x
        this.y0 := y
    }

    refresh_pos(game_width, game_height) {
        if this.x0 != '' {
            this.x := this.x0 * game_width / 2560
        }
        if this.y0 != '' {
            this.y := this.y0 * game_height / 1440
        }
    }
}



;---------------------------脚本本身代码------------------------------
class Dispatch {
    static p_area_range_1 := Point(500, 160)
    static p_area_range_2 := Point(1800, 1280)
    static p_dispatch_button := Point(2465, 1360)
    static characters := [Point(600, 240), Point(600, 384), Point(600, 528), Point(600, 672), Point(600, 816), Point(600, 960), Point(600, 1104)]
    static dispatch_countries := [Point(200, 200), Point(200, 320), Point(200, 400), Point(200, 480),Point(200, 200)]
    static p_dispatch_icon := Point(102, 60)
    static p_choose_character_icon := Point(25, 80)
    static color_off_white := '0xECE5D8'
	static color_off_red := '0xDC6148'
    static color_yellow_choose_character_icon := '0x263240'
    static color_green_under_avatar := '0xD3E6AE'
	static color_green_under_avatar2 := '0xD3E5AE'
    static sleep_time := 100
	static sleep_time1 := 300

    static refresh_pos() {
        size := Genshin.get_game_pos()
        width := size[1]
        height := size[2]
        this.p_area_range_1.refresh_pos(width, height)
        this.p_area_range_2.refresh_pos(width, height)
        this.p_dispatch_button.refresh_pos(width, height)
        for i in this.characters {
            i.refresh_pos(width, height)
        }
        for i in this.dispatch_countries {
            i.refresh_pos(width, height)
        }
        this.p_dispatch_icon.refresh_pos(width, height)
        this.p_choose_character_icon.refresh_pos(width, height)
    }

    static dispatch() {
        this.refresh_pos()
        if PixelGetColor((this.p_dispatch_button.x, this.p_dispatch_button.y) = this.color_off_white or this.p_dispatch_button.x, this.p_dispatch_button.y = this.color_off_red ) and PixelGetColor(this.p_dispatch_icon.x, this.p_dispatch_icon.y) = this.color_off_white  {
            size := Genshin.get_game_pos()
            width := size[1]
            height := size[2]
			for country in this.dispatch_countries {
                MouseClick(, country.x, country.y)
                Sleep(this.sleep_time)
				i := 0
				; 重试次数为5
                while i < 5 and (PixelSearch(&x, &y, this.p_area_range_1.x, this.p_area_range_1.y, this.p_area_range_2.x, this.p_area_range_2.y, this.color_green_under_avatar, 5) or PixelSearch(&x, &y, this.p_area_range_1.x, this.p_area_range_1.y, this.p_area_range_2.x, this.p_area_range_2.y, this.color_green_under_avatar2, 5)) {
                    MouseClick(, x, y)
                    Sleep(this.sleep_time1)
                    MouseClick(, this.p_dispatch_button.x, this.p_dispatch_button.y)
                    Sleep(this.sleep_time1)
                    MouseClick(, this.p_dispatch_button.x, this.p_dispatch_button.y)
                    Sleep(this.sleep_time1)
                    MouseClick(, this.p_dispatch_button.x, this.p_dispatch_button.y)
                    Sleep(this.sleep_time1)
                    ; 选人
                    for character in this.characters {
                        mouseClick(, character.x, character.y)
                        Sleep(this.sleep_time1)
						j := 0 
                        if PixelGetColor(this.p_choose_character_icon.x, this.p_choose_character_icon.y) != this.color_yellow_choose_character_icon {
                            break
                        }
                    }
					i++
					Sleep(this.sleep_time)
                }
				

            }
            
            ;TipOnce.tip('完成', , )
			ToolTip('完成', width / 2, height / 2, 3)
			;mouseClick(, this.p_area_range_2.x, this.p_area_range_2.y) ;点击测试2
			 Sleep(1500)
			Send ("{esc}") 
        } else {
            size := Genshin.get_game_pos()
            width := size[1]
            height := size[2]
			ToolTip('当前不是派遣界面', width / 2, height / 2, 3)
            ;TipOnce.tip('当前不是派遣界面', , width / 2, height / 2)
			;mouseClick(, this.p_choose_character_icon.x, this.p_choose_character_icon.y) ;这里是位置点击测试
			Sleep(1500)
        }
    }
}

; ---执行---
;WinActive('原神')
WinWaitActive('原神')
;WinWaitActive (,'ahk_exe YuanShen.exe')
Dispatch.dispatch()


