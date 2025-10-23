# Connect to Atlas and fetch digger_db collection via mongoexport
mongoexport \
  --uri "mongodb+srv://diggerfdf:passwd@cluster0.ro0c4tj.mongodb.net/clash_royale_manager?retryWrites=true&w=majority&appName=Cluster0" \
  --collection digger_db \
  --out digger_db.json \
  --jsonArray

# Remove all _id lines from the exported JSON using sed
sed -E '/"_id": \{ "\$oid": "[^"]+" \},?/d' digger_db.json > digger_db_clean.json
