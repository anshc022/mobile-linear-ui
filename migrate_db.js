
const { Pool } = require('pg');

const pool = new Pool({
  connectionString: 'postgresql://neondb_owner:npg_3sfBPupIrdX0@ep-empty-base-a45izwen-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
  ssl: {
    rejectUnauthorized: false
  }
});

async function migrate() {
  try {
    const client = await pool.connect();
    
    console.log('Adding last_notified_status column...');
    await client.query(`
      ALTER TABLE client_requests 
      ADD COLUMN IF NOT EXISTS last_notified_status VARCHAR(50);
    `);
    
    // Initialize it to match current status for existing records so we don't spam notifications for old stuff
    console.log('Initializing last_notified_status for existing records...');
    await client.query(`
      UPDATE client_requests 
      SET last_notified_status = status 
      WHERE last_notified_status IS NULL;
    `);
    
    console.log('Migration complete.');
    client.release();
    pool.end();
  } catch (err) {
    console.error('Migration failed:', err);
    process.exit(1);
  }
}

migrate();
