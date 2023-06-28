use std::collections::HashSet;

const ROWS: usize = 5;
const WIDTH: usize = 16;
const GROUPS: usize = WIDTH / 2;
const TRACKS: usize = 9;

const KEY_UNIT: f64 = 0.75 * 25.4;

macro_rules! words {
    { $($word:tt)* } => { vec![ $( stringify!($word), )* ] }
}

struct Key {
    name: &'static str,
    u: f64, // 0.75 in
    x: f64, // mm
    y: f64, // mm
    group: usize,
    track: usize,
}

type Keyboard = Vec<Vec<Key>>;

fn expand_keyboard() -> Keyboard {
    let key_names = vec![
        words![ ESC 1 2 3 4 5 6 7 8 9 0 MINUS EQUAL BSLS GRAVE F16 ],
        words![ TAB  Q W E R T Y U I O P        LBRC RBRC BSPC F17 ],
        words![ LCTL  A S D F G H J K L       SCLN QUOTE ENTER F18 ],
        words![ LSFT   Z X C V B N M   COMMA DOT SLASH RSFT UP F19 ],
        words![ LFN LALT LGUI SPACE  RGUI RCTL RFN LEFT DOWN RIGHT ],
    ];

    let key_groups = vec![
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7],
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7],
        vec![0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7],
        vec![0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7],
        vec![0, 0, 1, 3, 4, 5, 6, 6, 7, 7],
    ];

    let key_tracks = vec![
        vec![0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        vec![2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
        vec![5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
        vec![6, 7, 6, 7, 6, 7, 6, 7, 6, 7, 6, 6, 6, 5],
        vec![7, 8, 8, 8, 8, 8, 8, 7, 8, 7],
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
        let y = row as f64 * KEY_UNIT;

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

            x += u * KEY_UNIT;
        }
    }

    kb
}

fn main() {
    let kb = expand_keyboard();
    // quick 'n' dirty KLE
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
