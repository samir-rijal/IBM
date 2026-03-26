mkdir -p ~/.streamlit/

echo "\[general]\nemail = \"nirmalkchhetri.dev@gmail.com\"\n\n" > ~/.streamlit/credentials.toml
echo "\n[server]\nheadless = true\nport = \$PORT\nenableCORS = false\n\n" > ~/.streamlit/config.toml