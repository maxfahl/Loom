
import argparse
import os
import sys
from pathlib import Path

def generate_nestjs_resource(name: str, project_path: str):
    """
    Generates a new NestJS resource (module, controller, service, DTOs, and basic tests).

    Args:
        name (str): The name of the resource (e.g., 'users', 'products').
        project_path (str): The root path of the NestJS project.
    """
    resource_name_singular = name.lower().rstrip('s')
    resource_name_plural = name.lower()
    resource_name_capitalized = resource_name_singular.capitalize()

    resource_dir = Path(project_path) / 'src' / resource_name_plural
    resource_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating NestJS resource '{resource_name_plural}' in {resource_dir}...")

    # DTOs directory
    dto_dir = resource_dir / 'dto'
    dto_dir.mkdir(exist_ok=True)

    # Create DTO file
    create_dto_content = f"""
import {{{{ IsString, IsNotEmpty, IsOptional, IsEmail, MinLength }}}} from 'class-validator';
import {{{{ ApiProperty }}}} from '@nestjs/swagger';

export class Create{resource_name_capitalized}Dto {{
  @ApiProperty({{{{ description: 'The name of the {resource_name_singular}' }}}} )
  @IsString()
  @IsNotEmpty()
  name: string;

  @ApiProperty({{{{ description: 'The email of the {resource_name_singular}', required: false }}}} )
  @IsOptional()
  @IsEmail()
  email?: string;

  // Add other properties as needed
}}
"""
    (dto_dir / f'create-{resource_name_singular}.dto.ts').write_text(create_dto_content)

    update_dto_content = f"""
import {{{{ IsString, IsOptional, IsEmail, MinLength }}}} from 'class-validator';
import {{{{ ApiProperty }}}} from '@nestjs/swagger';
import {{{{ PartialType }}}} from '@nestjs/mapped-types';
import {{{{ Create{resource_name_capitalized}Dto }}}} from './create-{resource_name_singular}.dto';

export class Update{resource_name_capitalized}Dto extends PartialType(Create{resource_name_capitalized}Dto) {{
  @ApiProperty({{{{ description: 'The updated name of the {resource_name_singular}', required: false }}}} )
  @IsOptional()
  @IsString()
  @MinLength(3)
  name?: string;

  @ApiProperty({{{{ description: 'The updated email of the {resource_name_singular}', required: false }}}} )
  @IsOptional()
  @IsEmail()
  email?: string;

  // Add other properties as needed
}}
"""
    (dto_dir / f'update-{resource_name_singular}.dto.ts').write_text(update_dto_content)

    # Create Service file
    service_content = f"""
import {{{{ Injectable, NotFoundException }}}} from '@nestjs/common';
import {{{{ Create{resource_name_capitalized}Dto }}}} from './dto/create-{resource_name_singular}.dto';
import {{{{ Update{resource_name_capitalized}Dto }}}} from './dto/update-{resource_name_singular}.dto';

@Injectable()
export class {resource_name_capitalized}sService {{
  private readonly {resource_name_singular}s: any[] = []; // Replace with actual data source (e.g., database model)
  private nextId = 1;

  create(create{resource_name_capitalized}Dto: Create{resource_name_capitalized}Dto) {{
    const new{resource_name_capitalized} = {{{{ id: this.nextId++, ...create{resource_name_capitalized}Dto }}}};
    this.{resource_name_singular}s.push(new{resource_name_capitalized});
    return new{resource_name_capitalized};
  }}

  findAll() {{
    return this.{resource_name_singular}s;
  }}

  findOne(id: number) {{
    const {resource_name_singular} = this.{resource_name_singular}s.find(item => item.id === id);
    if (!{resource_name_singular}) {{
      throw new NotFoundException(`{resource_name_capitalized} with ID ${{id}} not found`);
    }}
    return {resource_name_singular};
  }}

  update(id: number, update{resource_name_capitalized}Dto: Update{resource_name_capitalized}Dto) {{
    const index = this.{resource_name_singular}s.findIndex(item => item.id === id);
    if (index === -1) {{
      throw new NotFoundException(`{resource_name_capitalized} with ID ${{id}} not found`);
    }}
    this.{resource_name_singular}s[index] = {{{{ ...this.{resource_name_singular}s[index], ...update{resource_name_capitalized}Dto }}}};
    return this.{resource_name_singular}s[index];
  }}

  remove(id: number) {{
    const index = this.{resource_name_singular}s.findIndex(item => item.id === id);
    if (index === -1) {{
      throw new NotFoundException(`{resource_name_capitalized} with ID ${{id}} not found`);
    }}
    const removed{resource_name_capitalized} = this.{resource_name_singular}s.splice(index, 1);
    return removed{resource_name_capitalized}[0];
  }}
}}
"""
    (resource_dir / f'{resource_name_plural}.service.ts').write_text(service_content)

    # Create Controller file
    controller_content = f"""
import {{{{ Controller, Get, Post, Body, Patch, Param, Delete, HttpCode, HttpStatus }}}} from '@nestjs/common';
import {{{{ ApiTags, ApiOperation, ApiResponse, ApiBody }}}} from '@nestjs/swagger';
import {{{{ {resource_name_capitalized}sService }}}} from './{resource_name_plural}.service';
import {{{{ Create{resource_name_capitalized}Dto }}}} from './dto/create-{resource_name_singular}.dto';
import {{{{ Update{resource_name_capitalized}Dto }}}} from './dto/update-{resource_name_singular}.dto';

@ApiTags('{resource_name_plural}')
@Controller('{resource_name_plural}')
export class {resource_name_capitalized}sController {{
  constructor(private readonly {resource_name_singular}sService: {resource_name_capitalized}sService) {{}}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({{{{ summary: 'Create a new {resource_name_singular}' }}}} )
  @ApiResponse({{{{ status: HttpStatus.CREATED, description: 'The {resource_name_singular} has been successfully created.' }}}} )
  @ApiResponse({{{{ status: HttpStatus.BAD_REQUEST, description: 'Invalid input data.' }}}} )
  @ApiBody({{{{ type: Create{resource_name_capitalized}Dto }}}} )
  create(@Body() create{resource_name_capitalized}Dto: Create{resource_name_capitalized}Dto) {{
    return this.{resource_name_singular}sService.create(create{resource_name_capitalized}Dto);
  }}

  @Get()
  @ApiOperation({{{{ summary: 'Retrieve all {resource_name_plural}' }}}} )
  @ApiResponse({{{{ status: HttpStatus.OK, description: 'Successfully retrieved list of {resource_name_plural}.' }}}} )
  findAll() {{
    return this.{resource_name_singular}sService.findAll();
  }}

  @Get(':id')
  @ApiOperation({{{{ summary: 'Retrieve a single {resource_name_singular} by ID' }}}} )
  @ApiResponse({{{{ status: HttpStatus.OK, description: 'Successfully retrieved {resource_name_singular}.' }}}} )
  @ApiResponse({{{{ status: HttpStatus.NOT_FOUND, description: '{resource_name_capitalized} not found.' }}}} )
  findOne(@Param('id') id: string) {{
    return this.{resource_name_singular}sService.findOne(+id);
  }}

  @Patch(':id')
  @ApiOperation({{{{ summary: 'Update an existing {resource_name_singular} by ID' }}}} )
  @ApiResponse({{{{ status: HttpStatus.OK, description: 'The {resource_name_singular} has been successfully updated.' }}}} )
  @ApiResponse({{{{ status: HttpStatus.NOT_FOUND, description: '{resource_name_capitalized} not found.' }}}} )
  @ApiResponse({{{{ status: HttpStatus.BAD_REQUEST, description: 'Invalid input data.' }}}} )
  @ApiBody({{{{ type: Update{resource_name_capitalized}Dto }}}} )
  update(@Param('id') id: string, @Body() update{resource_name_capitalized}Dto: Update{resource_name_capitalized}Dto) {{
    return this.{resource_name_singular}sService.update(+id, update{resource_name_capitalized}Dto);
  }}

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({{{{ summary: 'Delete a {resource_name_singular} by ID' }}}} )
  @ApiResponse({{{{ status: HttpStatus.NO_CONTENT, description: 'The {resource_name_singular} has been successfully deleted.' }}}} )
  @ApiResponse({{{{ status: HttpStatus.NOT_FOUND, description: '{resource_name_capitalized} not found.' }}}} )
  remove(@Param('id') id: string) {{
    this.{resource_name_singular}sService.remove(+id);
  }}
}}
"""
    (resource_dir / f'{resource_name_plural}.controller.ts').write_text(controller_content)

    # Create Module file
    module_content = f"""
import {{{{ Module }}}} from '@nestjs/common';
import {{{{ {resource_name_capitalized}sController }}}} from './{resource_name_plural}.controller';
import {{{{ {resource_name_capitalized}sService }}}} from './{resource_name_plural}.service';

@Module({{{{
  controllers: [{resource_name_capitalized}sController],
  providers: [{resource_name_capitalized}sService],
}}}} )
export class {resource_name_capitalized}sModule {{}}
"""
    (resource_dir / f'{resource_name_plural}.module.ts').write_text(module_content)

    # Create Test file
    test_content = f"""
import {{{{ Test, TestingModule }}}} from '@nestjs/testing';
import {{{{ {resource_name_capitalized}sController }}}} from './{resource_name_plural}.controller';
import {{{{ {resource_name_capitalized}sService }}}} from './{resource_name_plural}.service';
import {{{{ Create{resource_name_capitalized}Dto }}}} from './dto/create-{resource_name_singular}.dto';
import {{{{ Update{resource_name_capitalized}Dto }}}} from './dto/update-{resource_name_singular}.dto';

describe('{resource_name_capitalized}sController', () => {{
  let controller: {resource_name_capitalized}sController;
  let service: {resource_name_capitalized}sService;

  beforeEach(async () => {{
    const module: TestingModule = await Test.createTestingModule({{{{
      controllers: [{resource_name_capitalized}sController],
      providers: [{resource_name_capitalized}sService],
    }}}}).compile();

    controller = module.get<{resource_name_capitalized}sController>({resource_name_capitalized}sController);
    service = module.get<{resource_name_capitalized}sService>({resource_name_capitalized}sService);
  }});

  it('should be defined', () => {{
    expect(controller).toBeDefined();
  }});

  describe('create', () => {{
    it('should create a {resource_name_singular}', () => {{
      const createDto: Create{resource_name_capitalized}Dto = {{{{ name: 'Test {resource_name_capitalized}', email: 'test@{resource_name_singular}.com' }}}};
      jest.spyOn(service, 'create').mockReturnValue({{{{ id: 1, ...createDto }}}});
      expect(controller.create(createDto)).toEqual({{{{ id: 1, ...createDto }}}});
    }});
  }});

  describe('findAll', () => {{
    it('should return an array of {resource_name_plural}', () => {{
      const result = [{{ id: 1, name: 'Test {resource_name_capitalized}' }}];
      jest.spyOn(service, 'findAll').mockReturnValue(result);
      expect(controller.findAll()).toEqual(result);
    }});
  }});

  describe('findOne', () => {{
    it('should return a single {resource_name_singular}', () => {{
      const result = {{ id: 1, name: 'Test {resource_name_capitalized}' }};
      jest.spyOn(service, 'findOne').mockReturnValue(result);
      expect(controller.findOne('1')).toEqual(result);
    }});
  }});

  describe('update', () => {{
    it('should update a {resource_name_singular}', () => {{
      const updateDto: Update{resource_name_capitalized}Dto = {{{{ name: 'Updated {resource_name_capitalized}' }}}};
      const result = {{ id: 1, name: 'Updated {resource_name_capitalized}' }};
      jest.spyOn(service, 'update').mockReturnValue(result);
      expect(controller.update('1', updateDto)).toEqual(result);
    }});
  }});

  describe('remove', () => {{
    it('should remove a {resource_name_singular}', () => {{
      jest.spyOn(service, 'remove').mockReturnValue({{{{ id: 1, name: 'Removed {resource_name_capitalized}' }}}});
      expect(controller.remove('1')).toBeUndefined();
    }});
  }});
}});
"""
    (resource_dir / f'{resource_name_plural}.controller.spec.ts').write_text(test_content)

    print(f"NestJS resource '{resource_name_plural}' generated successfully!")
    print(f"Remember to import {resource_name_capitalized}sModule into your AppModule (src/app.module.ts) and install dependencies: npm install class-validator class-transformer @nestjs/swagger swagger-ui-express @nestjs/mapped-types")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a new NestJS resource (module, controller, service, DTOs, tests).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "name",
        help="The name of the resource to generate (e.g., 'users', 'products').
"
             "The script will automatically handle singular/plural and capitalization."
    )
    parser.add_argument(
        "--project-path",
        default=".",
        help="The root path of the NestJS project (default: current directory)."
    )

    args = parser.parse_args()

    # Basic validation for project_path
    if not (Path(args.project_path) / 'src').is_dir():
        print(f"Error: '{args.project_path}/src' directory not found. "
              "Please ensure you are running this script from the NestJS project root "
              "or provide the correct --project-path.", file=sys.stderr)
        sys.exit(1)

    generate_nestjs_resource(args.name, args.project_path)
