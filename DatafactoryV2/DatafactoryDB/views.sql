create view frame_header_view as
	select frame.id,frame.file_name,header_definition.name, header_definition.version,coalesce( header.string_value, header.long_value,header.double_value) as value ,
	header_definition.data_type,header_definition.comment ,header.extension,header.order_keyword 
	from frame 
	left join header on (header.id_frame =frame.id) 
	left join header_definition_header on (header.id= header_definition_header.id_header) 
	left join header_definition on ( header_definition.id=header_definition_header.id_header_definition) 
	order by header.extension, header.order_keyword

create view frame_view as 
	select frame.id, camera.instrument, observation_mode.mode, frame.observation_date, frame.observation_date_microsecond, frame.exposition_time, frame.state,
	frame.is_raw, frame.id_program, frame.id_observation_block, frame.path, frame.filename, frame.number_extensions, frame.number_frame, frame.id_principal_investigator,
	frame.radeg, frame.decdeg
	from frame
	left join camera on (camera.id = frame.id_camera)
	left join observation_mode on (observation_mode.id = frame.id_observation_mode)

create view osiris_header_view as
	select header.id_frame, header_definition.name, header_definition.version, coalesce( header.string_value, header.long_value,header.double_value) as value,
	header_definition.data_type,header_definition.comment ,header.extension,header.order_keyword 
	from header_definition
	left join header_definition_header on (header_definition.id= header_definition_header.id_header_definition)  
	left join header on (header_definition_header.id_header =header.id)
	where camera.id = 1 
	order by header.extension, header.order_keyword

create view canaricam_header_view as
	select header.id_frame,header_definition.name, header_definition.version,coalesce( header.string_value, header.long_value,header.double_value) as value,
	header_definition.data_type,header_definition.comment ,header.extension,header.order_keyword 
	from header_definition
	left join header_definition_header on (header_definition.id= header_definition_header.id_header_definition)  
	left join header on (header_definition_header.id_header =header.id)
	where camera.id = 6
	order by header.extension, header.order_keyword

/*select header.id_frame, header_definition.name, coalesce( header.string_value, header.long_value,header.double_value) as value, 
header_definition.data_type,header_definition.comment ,header.extension,header.order_keyword  
from header_definition 
left join header_definition_header on (header_definition.id= header_definition_header.id_header_definition)  
left join header on (header_definition_header.id_header =header.id) 
where header_definition.id_camera = 1 and name='ROI_4Y'\G*/
