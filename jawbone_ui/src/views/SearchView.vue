<script>
import axios from 'axios'

export default {
  data() {
    return {
    path_map: {
      "None": "",
      "Character": "http://0.0.0.0:8000/characters/", 
      "Clue": "http://0.0.0.0:8000/reference-info/", 
      "Page": "http://0.0.0.0:8000/page-info/",
    },
    selected: '',
    selected_name: '',
    has_name: false,
    has_role: false,
    has_page: false,
    has_clue: false,
    has_record_id: false,
    has_info: false,
    has_link: false,
    name: '',
    search_name: '',
    role: '',
    search_role: '',
    page: '',
    search_page: '',
    clue: '',
    id: '',
    search_id: '',
    info: '',
    link: '',
    search_values: {},
    character_results: {},
    page_results: {},
    ref_info_results: {},
    ref_info: '',
    edit_record: {},
    new_record: {},
    post_results: {},
    delete_results: {},
    edit_results: {},
    returned_records: [],
    edit_mode: false,
    edit_fields: [],
    insert_mode: false,
    fields: [],
    new_row_data: []
  };
  },
  methods: {
    setFields(fields) {
      this.has_record_id = false
      this.has_name = false
      this.has_role = false
      this.has_page = false
      this.has_clue = false
      this.has_reference_info = false
      fields.forEach(field => {
        if (
          field === "id"
        ) {this.id = true} else (
          this[field] = true
        )
      console.log("Fields in setFields", fields)
      });
    },
    hasFields (field) {
      return this.fields.includes(field)
    },
    async onChange(event) {
      // get the selected resource type value and hit the path to pull back all the records of that type
      this.fields = []
      console.log("Event target: ", event.target.value)
      this.selected_name = event.target.value // Record type
      this.selected = this.path_map[event.target.value] // URL for get records
      this.returned_records = (await axios.get(this.selected)).data.results
      console.log("records ", this.returned_records, "index 0 ", Object.keys(this.returned_records[0]))
      // fields for selected record type
      this.fields = (await axios.get("http://0.0.0.0:8000/fields/" + this.selected_name)).data.results
      console.log("fields ", this.fields)
      this.setFields(this.fields)
    },
    deleteFactory (resourceId) { // TODO not updating returned_records yet
        console.log("Checking delete: ", this.selected, resourceId)
        const headers = {"headers": {
                  'content-type': 'application/json',
                  'Accept': 'application/json'
                }
            }

        axios.delete(this.selected + resourceId, headers).then((delete_res) => {
            this.delete_results = delete_res.data.results
        })
        .catch((error) => {
            console.error(error);
        });
    },
    toggleInsert() {
      this.insert_mode = !this.insert_mode
      if (this.insert_mode) this.edit_mode = false
    },
    toggleEdit() {
      this.edit_mode = !this.edit_mode
      if (this.edit_mode) this.insert_mode = false
    },
    async clearSearch() {
      // Clear search terms and retrieve recent records for selected record type.
      this.search_id = ''
      this.search_name = ''
      this.search_page = ''
      this.search_role = ''
      this.returned_records = await (await axios.get(this.selected)).data.results
    },
    async addFactory () {
      this.toggleInsert()
    },
    async addRecord (new_record) {
      // 
      this.fields.forEach((field) => {
        console.log("this.fields values ", this[field])
      })
      this.fields.forEach((field) => {
        new_record[field] = this[field]
      }) 
      this.new_row_data = await (await axios.post(this.selected, new_record)).data.results
      this.returned_records = await (await axios.get(this.selected)).data.results
      this.toggleInsert()
    },
    async editFactory (resource_id) {
      this.toggleEdit()
      this.edit_record = await (await axios.get(this.selected + resource_id)).data.results
      this.edit_fields = Object.keys(this.edit_record)
      this.edit_fields.forEach((field) => {
          this[field] = this.edit_record[field]
      })  
    },
    async saveEdit (record) {
      console.log("Edit record check: ", record)
      // set value of edited record field to input value
      this.fields.forEach((field) => {
        record[field] = this[field]
      }) 
      this.edit_results = await (await axios.post(this.selected + record.id, record)).data.results
      // Update records shown
      this.returned_records = await (await axios.get(this.selected)).data.results
      this.toggleEdit()
    },
    async searchRecords() {

      this.search_values["selected_name"] = this.selected_name
      this.search_values['id'] = (this.search_id || null)
      this.search_values['name'] = (this.search_name || null)
      this.search_values['role'] = (this.search_role || null)
      this.search_values['page'] = (this.search_page || null)

      this.returned_records = await (await axios.post("http://0.0.0.0:8000/search/", this.search_values)).data.results
  },
  },
};
</script>

<template>
  <main>
      <div>
      <select @change="onChange"> 
        <option disabled value="">Select record type</option>
        <option v-for="(resource_path, resource_type) in path_map" :key="resource_type" :value="resource_type"> {{ resource_type }}</option>
      </select>
    </div>
    <div v-if="selected">
      <label v-if="hasFields('id')">Search by ID: <input type="text" v-model="search_id"/></label>
      <label v-if="hasFields('name')">Name: <input type="text" v-model="search_name"/></label>
      <label v-if="hasFields('role')">Role: <input type="text" v-model="search_role"/></label>
      <label v-if="hasFields('page')">Page: <input type="text" v-model="search_page"/></label>
      <button @click="searchRecords()">Submit search</button><button @click="clearSearch()">Clear search</button>
    </div>
    <table v-if="returned_records"> 
        <thead>
            <tr> 
                <td v-if="hasFields('id')">Record ID</td>
                <td v-if="hasFields('name')">Name</td>
                <td v-if="hasFields('role')">Role</td>
                <td v-if="hasFields('page')">Page</td>
                <td v-if="hasFields('clue')">Clue</td>
                <td v-if="hasFields('info')">Reference info</td>
                <td v-if="hasFields('link')">Link</td>
            </tr>
       </thead>
       <tbody>
            <tr v-for="(item, index) in returned_records" :key="index"  >
            <td v-if="hasFields('id')">{{item.id}}</td>
            <td v-if="hasFields('name')">{{item.name}}</td>
            <td v-if="hasFields('role')">{{item.role}}</td>
            <td v-if="hasFields('page')">{{item.page}}</td>
            <td v-if="hasFields('clue')">{{item.clue}}</td>
            <td v-if="hasFields('info')">{{item.info}}</td>
            <td v-if="hasFields('link')">{{item.link}}</td>
            <td><button @click="deleteFactory(item.id)">delete</button><button @click="editFactory(item.id)">edit</button></td>
            </tr> 
       </tbody>
    
    </table>   
    <div v-if="edit_mode">
      <label v-if="edit_fields.includes('name')">Name: <input type="text" v-model="name"/></label>
      <label v-if="edit_fields.includes('role')">Role: <input type="text" v-model="role"/></label>
      <label v-if="edit_fields.includes('page')">Page: <input type="text" v-model="page"/></label>
      <label v-if="edit_fields.includes('clue')">Clue: <input type="text" v-model="clue"/></label>
      <label v-if="edit_fields.includes('info')">Reference Info: <input type="text" v-model="info"/></label>
      <label v-if="edit_fields.includes('link')">Reference link: <input type="text" v-model="link"/></label>
      
      <button @click="saveEdit(edit_record)">save</button>

    </div>
    <div v-if="selected">
      <button @click="addFactory()">New record</button>
      <div v-if="insert_mode">
        
        <label v-if="this.fields.includes('name')">Name: <input type="text" v-model="name"/></label>
        <label v-if="this.fields.includes('role')">Role: <input type="text" v-model="role"/></label>
        <label v-if="this.fields.includes('page')">Page: <input type="text" v-model="page"/></label>
        <label v-if="this.fields.includes('clue')">Clue: <input type="text" v-model="clue"/></label>
        <label v-if="this.fields.includes('info')">Reference info: <input type="text" v-model="info"/></label>
        <label v-if="this.fields.includes('link')">Reference link: <input type="text" v-model="link"/></label>
        
        <button @click="addRecord(this.new_record)">Save</button>
      </div>
    </div>

  </main>
</template>
