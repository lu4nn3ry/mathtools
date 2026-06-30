use tauri::Manager;

#[tauri::command]
fn solve(expression: String) -> String {
    format!("Solve requested: {}", expression)
}

#[tauri::command]
fn export(content: String, format: String) -> String {
    format!("Export as {}: {} chars", format, content.len())
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Bem-vindo, {}! MathTools Offline pronto.", name)
}

pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![solve, export, greet])
        .setup(|app| {
            let _window = app.get_webview_window("main").unwrap();

            // Spawn the Python FastAPI sidecar on app startup
            let sidecar_command = app.shell().sidecar("backend")
                .expect("failed to create sidecar command")
                .env("PYTHONUTF8", "1")
                .env("PYTHONIOENCODING", "utf-8");

            // We spawn but don't await — the sidecar runs independently.
            // The frontend communicates with it via HTTP at localhost:8080.
            match sidecar_command.spawn() {
                Ok((_rx, _child)) => {
                    println!("[sidecar] Python backend spawned successfully");
                    // Keep _child alive: when it drops, the process is killed.
                    // Store in app state if we need to manage lifecycle.
                    std::mem::forget(_child);
                }
                Err(e) => {
                    eprintln!("[sidecar] Failed to spawn Python backend: {e}");
                    // Non-fatal: the frontend will show offline state.
                }
            }

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
