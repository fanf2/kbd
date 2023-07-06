use std::collections::HashSet;

const MM_IN: f64 = 25.4;
const KEY_UNIT: f64 = 0.75 * MM_IN;

const SCREW_HOLE: f64 = 3.0;
const RIVET_HOLE: f64 = 5.0;
const SWITCH_HOLE: f64 = 14.0;


const ROWS: usize = 5;
const WIDTH: usize = 16;
const GROUPS: usize = WIDTH / 2;
const TRACKS: usize = 9;


macro_rules! words {
    { $($word:tt)* } => { vec![ $( stringify!($word), )* ] }
}

struct Key {
    name: &'static str,
    u: f64, // 0.75 in
    x: f64, // 0.75 in
    y: f64, // 0.75 in
    group: usize,
    track: usize,
}

type Keyboard = Vec<Vec<Key>>;

fn expand_keyboard() -> Keyboard {
    let key_names = vec![
        words![ ESC 1 2 3 4 5 6 7 8 9 0 MINUS EQUAL BSLS GRAVE F13 ],
        words![ TAB  Q W E R T Y U I O P        LBRC RBRC BSPC F14 ],
        words![ LCTL  A S D F G H J K L       SCLN QUOTE ENTER F15 ],
        words![ LSFT   Z X C V B N M   COMMA DOT SLASH RSFT UP F16 ],
        words![ LFN LALT LGUI SPACE  RGUI RCTL RFN LEFT DOWN RIGHT ],
    ];

    let key_groups = vec![
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7],
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 7],
        vec![0, 1, 2, 3, 4, 5, 6, 6, 7, 7],
    ];

    let key_tracks = vec![
        vec![0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        vec![2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
        vec![5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
        vec![6, 7, 6, 7, 6, 7, 6, 7, 6, 7, 6, 6, 6, 5],
        vec![8, 8, 8, 8, 8, 8, 8, 7, 8, 7],
    ];

    // consistent number of rows
    assert!(key_names.len() == ROWS);
    assert!(key_groups.len() == ROWS);
    assert!(key_tracks.len() == ROWS);

    let mut kb: Vec<Vec<Key>> = vec![];
    let mut matrix = [[false; TRACKS]; GROUPS];
    let mut name_set = HashSet::new();

    for row in 0..ROWS {
        kb.push(vec![]);
        let len = key_names[row].len();

        // correct length of rows
        assert!(key_groups[row].len() <= WIDTH);

        // consistent length of rows
        assert!(key_groups[row].len() == len);
        assert!(key_tracks[row].len() == len);

        let mut x = 0.0;
        let y = row as f64;

        for k in 0..len {
            let name = key_names[row][k];
            let group = key_groups[row][k];
            let track = key_tracks[row][k];

            // unique names
            assert!(!name_set.contains(name));
            name_set.insert(name);

            // valid group and track numbers
            assert!(group < GROUPS);
            assert!(track < TRACKS);

            // unique matrix positions
            let pos = &mut matrix[group][track];
            assert!(!*pos);
            *pos = true;

            let u = match key_names[row][k] {
                "SPACE" => 6.25,
                "LSFT" | "ENTER" => 2.25,
                "LCTL" | "RSFT" => 1.75,
                "TAB" | "BSPC" => 1.5,
                "LFN" | "LALT" | "LGUI" => 1.25,
                _ => 1.0,
            };

            kb[row].push(Key { name, group, track, x, y, u });

            x += u;
        }
    }

    kb
}

fn print_kle(kb: &Keyboard) {
    let mut rowsep = "";
    for row in 0..ROWS {
        print!("{rowsep}[");
        let mut keysep = "";
        for key in &kb[row] {
            let u = key.u;
            let name = key.name;
            let track = key.track;
            let group = key.group;
            print!(
                "{keysep}\
                {{w:{u}}},\"{track},{group}\
                \\n\\n\\n\\n\\n\\n\\n\\n\\n\
                {name}\""
            );
            keysep = ",";
        }
        print!("]");
        rowsep = ",\n";
    }
    print!("\n");
}

// elegant mapping from groups/cols and tracks/rows to GPIO pins
fn print_qmk_matrix() {
    print!(r#"
    "diode_direction": "COL2ROW",
    "matrix_pins": {{
"#);
    print!(r#"        "cols":"#);
    let mut sep = " [";
    for col in 0 ..= 8 {
        print!("{sep}\"GP{col}\"");
        sep = ", ";
    }
    println!("],");
    print!(r#"        "rows":"#);
    let mut sep = " [";
    for row in 0 ..= 6 {
        print!("{sep}\"GP{row}\"");
        sep = ", ";
    }
    println!(r#", "GP26"]"#);
    println!("    }},");
}

fn print_qmk_layout(kb: &Keyboard) {
    let mut keysep = "[\n";
    print!(r#"
    "layouts": {{
        "LAYOUT_65_ansi_split_bs": {{
            "layout": "#);
    for row in 0..ROWS {
        for key in &kb[row] {
            let u = key.u;
            let x = key.x;
            let y = key.y;
            let name = key.name;
            let track = key.track;
            let group = key.group;
            print!("{keysep}                {{ \
                    \"label\": \"{name}\", \
                    \"matrix\": [{track},{group}], \
                    \"x\": {x}, \
                    \"y\": {y}, \
                    \"w\": {u} \
                    }}");
            keysep = ",\n";
        }
    }
    print!("\n            ]\n        }}\n   }}\n");
}

fn main() {
    let kb = expand_keyboard();
    //print_kle(&kb);
    print_qmk_matrix();
    print_qmk_layout(&kb);
}
